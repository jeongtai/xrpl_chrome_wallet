from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, GenericAPIView, CreateAPIView
from rest_framework.response import Response

# Create your views here.

# Define the network client
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait, XRPLReliableSubmissionException
from xrpl.utils import xrp_to_drops
from api.models import ACCOUNT
from api.serializers import ACCOUNTSerializer, SENDXRP
import json

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)
from xrpl.models.requests.account_info import AccountInfo

# Create a wallet using the testnet faucet:
# https://xrpl.org/xrp-testnet-faucet.html


def send_xrp(seed: str, amount: int, destination: str):
    sending_wallet = Wallet.from_seed(seed)
    receiving_wallet = Wallet.from_seed(destination)
    client = JsonRpcClient(JSON_RPC_URL)
    payment = Payment(
        account=sending_wallet.address,
        amount=xrp_to_drops(int(amount)),
        destination=receiving_wallet.address,
    )
    try:
        response = submit_and_wait(payment, client, sending_wallet)
    except XRPLReliableSubmissionException as e:
        response = f"Submit failed: {e}"
    return response


class ACCOUNTSCreateAPIView(RetrieveAPIView):
    queryset = ACCOUNT.objects.all()
    serializer_class = ACCOUNTSerializer

    def retrieve(self, request, *args, **kwargs):
        test_wallet = generate_faucet_wallet(client, debug=True)
        instance = ACCOUNT()
        instance.wallet_address = str(test_wallet.address)
        instance.private_key = str(test_wallet.private_key)
        instance.public_key = str(test_wallet.public_key)
        instance.seed = str(test_wallet.seed)
        acct_info = AccountInfo(
            account=instance.wallet_address,
            ledger_index="validated",
            strict=True,
        )
        res = client.request(acct_info)

        instance.balance = str(res.result['account_data']['Balance'])
        instance.save()
        serializer = self.get_serializer(instance=instance)

        return Response(serializer.data)


class SENDXRPView(CreateAPIView):
    queryset = ACCOUNT.objects.all()
    serializer_class = SENDXRP

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #제발 request.data를 쌩으로 다룰 생각하지 말고 일단 serializer를 쓰자
        sender = ACCOUNT.objects.get(wallet_address = serializer.validated_data['sender']['wallet_address'])
        receiver = ACCOUNT.objects.get(wallet_address = serializer.validated_data['receiver']['wallet_address'])
        response = send_xrp(sender.seed,10,receiver.seed)
        #response는 복잡한 객체, response.result는 딕셔너리
        return Response(response.result)


