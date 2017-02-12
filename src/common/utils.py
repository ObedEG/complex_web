from datetime import datetime
import pytz
from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    FMT = '%Y-%m-%d %H:%M:%S %Z%z'
    MONTERREY = pytz.timezone('America/Monterrey')

    @staticmethod
    def email_is_valid(email):
        """
        This method validate the email with ReGex
        :param email: the email input :)
        :return: True if the email fits good "good@email.structure.com"
        """
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False


    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the Login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password users sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def get_timezone():
        """
        :return: The current time, date and timezone
        """

        utc_dt = datetime.now(tz=pytz.utc)
        mty_time = utc_dt.astimezone(Utils.MONTERREY)
        # mty_time2 = mty_time.strftime(Utils.FMT)
        return mty_time

    @staticmethod
    def get_mtytime(date):
        return Utils.MONTERREY.localize(date)
