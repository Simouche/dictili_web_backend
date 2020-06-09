import random
import secrets

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


account_activation_token = TokenGenerator()


def generate_token():
    """
    generates a 32 characters length token, this is being used as access token
    :return:
    """
    return secrets.token_hex(32)


def generate_reset_token():
    """
    generates a 16 characters length token, this is being used as password reset token
    :return:
    """
    return secrets.token_hex(16)


def generate_random_code():
    """
    generates a 5 characters random code, this is being used as OTP
    :return:
    """
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
    random_alphabet = random.choice(alphabet)
    randoms = [random_alphabet]
    for i in range(4):
        randoms.append(str(random.randint(0, 9)))

    code = ''.join(randoms)

    return code


def generate_random_password():
    password = ''
    for i in range(3):
        password += generate_random_code()

    return password
