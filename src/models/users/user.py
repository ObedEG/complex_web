import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, name, last_name, employee_num, email, password, _id=None):
        self.name = name
        self.last_name = last_name
        self.employee_num = employee_num
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies  that an e-mail/password combo (as sent by the sites forms is valid or not
        :param email: The user's email
        :param password: a sha512 hashed password
        :return:True if valid, False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTIONS, {"email": email})  # Password in sha512 -> pbkdf2_sha512

        if user_data is None:
            #  Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            #  Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong")
        return True

    @staticmethod
    def register_user(name, last_name, employee_num, email, password):
        """
        This method registers a user e-mail and password.
        The password already comes hashed as  sha-512
        :param email: user's email (might be invalid)
        :param password: sha-512 hashed password
        :param name:
        :param last_name:
        :param employee_num:
        :return: True if registered successfully, or False otherwise (exception can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTIONS, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The email you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email does not have the right format.")

        User(name, last_name, employee_num, email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTIONS,
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'last_name': self.last_name,
            'employee_num': self.employee_num,
            'email': self.email,
            'password': self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTIONS, {"email": email}))

    @classmethod
    def find_id_by_email(cls, email):
        user = cls(**Database.find_one(UserConstants.COLLECTIONS, {"email": email}))
        return user._id
