import os

import pytest

from pycose.exceptions import CoseIllegalKeyType
from pycose.keys import RSAKey, CoseKey
from pycose.keys.keyops import SignOp
from pycose.keys.keyparam import KpKty, RSAKpE, RSAKpN, KpAlg, KpKeyOps, RSAKpD
from pycose.keys.keytype import KtySymmetric, KtyOKP, KtyEC2, KtyRSA


@pytest.mark.parametrize('bit_length', [512, 1024, 2048, 4096])
def test_rsa_key_generation(bit_length):
    key = RSAKey.generate_key(bit_length)


@pytest.mark.parametrize('bit_length', [512, 1024])
@pytest.mark.parametrize('kty', [KtyOKP, KtySymmetric, KtyEC2, 1, 4])
def test_fail_on_illegal_kty(bit_length, kty):
    params = {KpKty: kty}

    with pytest.raises(CoseIllegalKeyType) as excinfo:
        # we don't really care about the key values here
        _ = RSAKey(n=os.urandom(256), e=os.urandom(3), optional_params=params)

    assert "Illegal key type in RSA COSE Key" in str(excinfo.value)


def test_dict_operations_on_rsa_key():
    cose_key = {KpKty: KtyRSA, RSAKpE: os.urandom(4), RSAKpN: os.urandom(256), KpKeyOps: [SignOp]}

    key = CoseKey.from_dict(cose_key)

    assert KpKty in key
    assert RSAKpE in key
    assert RSAKpN in key
    assert RSAKpD not in key
    assert -1 in key
    assert -2 in key
    assert KpAlg not in key
    assert 'ALG' not in key
    assert 'KEY_OPS' in key

    del key['KEY_OPS']

    key['subject_name'] = 'signing key'
    assert 'subject_name' in key

    assert 'KEY_OPS' not in key
