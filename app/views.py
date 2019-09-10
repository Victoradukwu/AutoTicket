"""A module of app views"""
from datetime import datetime
import simplejson as json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.base_user import make_password, check_password
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Flight, Seat, Ticket
from .utils.enums import SeatStatus
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserSerializer,
    FlightSerializer,
    SeatSerializer,
    TicketSerializer,
    LoginSerializer,
    RegisterSerializer,
    BookingSerializer,
    PaymentSerializer

)
from .utils.helpers import (
    generate_token,
    upload_image,
    send_email,
    make_payment,
    update_seat_status,
    FlightFilter,
    TicketFilter,
    IsAdminUserOrReadOnly,
    IsAdminUserOrOwnerReadOnly,
    IsAdminUserOrOwnerReadAndUpdateOnly
)


@api_view(['GET'])
def welcome(request):
    return render(request, 'app/welcome.html')


@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, JSONParser))
def user_signup(request):
    """
    Endpoint to register a user

    """
    data = request.data

    if data.get('password') == data.get('confirm_password'):
        data = data.copy()
        img = data.get('image')
        data['image'] = upload_image(img)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(data.get('password'))
            serializer.validated_data['username'] = serializer.validated_data.get('email')
            serializer.save()

            payload = {
                        'message': "Successfully signed up",
                        'data': serializer.data
                        }
            return Response(payload, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=LoginSerializer)
@api_view(['POST'])
@parser_classes((FormParser, MultiPartParser, JSONParser))
def user_signin(request):
    """
    Endpoint for user login

    """
    data = request.data

    user = get_object_or_404(User, email=data.get('email'))
    if check_password(data.get('password'), user.password):
        token = generate_token(user)
        payload = {
                    'message': "Successfully logged in",
                    'token': token,
                    'data': UserSerializer(user).data
                }
        payload['data']['isStaff'] = user.is_staff
        return Response(payload, status=status.HTTP_200_OK)
    return Response({'message': 'Wrong password or email'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=PaymentSerializer)
@api_view(['POST'])
@parser_classes((FormParser, JSONParser))
@permission_classes((IsAuthenticated, ))
def payment(request):
    """
    Endpoint to enable online payment using Paystack. Use the following card details.

    "pin": "1111",
    "number": "507850785078507812",
    "cvv": "081",
    "expiry_month": "12",
    "expiry_year":  "2020"
    """
    data = request.data
    serializer = PaymentSerializer(data=data)
    if serializer.is_valid():
        payment_data = {
            "email": serializer.validated_data.get('email', request.user.email),
            "amount": json.dumps(serializer.validated_data.get('amount')),
            "pin": serializer.validated_data.get('pin'),
            "card": {
                "number": serializer.validated_data.get('number'),
                "cvv": serializer.validated_data.get('cvv'),
                "expiry_month": serializer.validated_data.get('expiry_month'),
                "expiry_year":  serializer.validated_data.get('expiry_year')
            }
        }
        pay_resp = make_payment(payment_data)
        if pay_resp['data']['status'] != 'success':
            return Response({'message': pay_resp.data.display_text}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=BookingSerializer)
@api_view(['POST'])
@parser_classes((FormParser, JSONParser))
@permission_classes((IsAuthenticated, ))
def book_ticket(request):
    """
    Book flight ticket. Use the following card details

    "pin": "1111",
    "number": "507850785078507812",
    "cvv": "081",
    "expiry_month": "12",
    "expiry_year":  "2020"
    """
    data = request.data
    serializer = TicketSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['booked_by'] = request.user
        flight_id = serializer.validated_data.get('flight')
        flight = Flight.objects.get(number=flight_id)
        payment_data = {
            "email": serializer.validated_data.get('email', request.user.email),
            "amount": flight.fare,
            "pin": serializer.validated_data.get('pin'),
            "card": {
                "number": serializer.validated_data.get('number'),
                "cvv": serializer.validated_data.get('cvv'),
                "expiry_month": serializer.validated_data.get('expiry_month'),
                "expiry_year": serializer.validated_data.get('expiry_year')
            }
        }
        pay_resp = make_payment(payment_data)

        if pay_resp['data']['status'] == 'success':
            seat = Seat.objects.filter(status=1)[0]
            Ticket.objects.create(seat=seat, passenger=serializer.validated_data['passenger'], booked_by=request.user)
            update_seat_status(seat, SeatStatus.booked)

            flight_date = datetime.strftime(seat.flight.departure_time, '%Y-%m-%d %H:%M')
            flight_number = seat.flight.number
            seat_number = seat.seat_number
            mail_data = {
                'email': data.get('email'),
                'subject': 'Ticket Booking',
                'content': f'Ticket successfully booked\n date: {flight_date}\n flight no.: {flight_number}\n seat no.: {seat_number}'
            }

            send_email(mail_data)
            return Response({'message': 'Ticket successfully booked. Details have been sent by email'}, status=status.HTTP_200_OK)
        return Response({'message': pay_resp['data']['display_text']}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FlightList(generics.ListCreateAPIView):
    """
        get:
        Return the list of all flight objects

        post:
        creates a new flight object

        """

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filterset_class = FlightFilter


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    """

    get:
    Return the details of a single flight

    put:
    Updates a given flight, non-partial update

    patch:
    Updates a given flight, partial update



    delete:
    Deletes a single flight
    """

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class SeatList(generics.ListCreateAPIView):
    """
        get:
        Return the list of all seat objects.

        post:
        creates a new seat object.

        """

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class SeatDetail(generics.RetrieveUpdateDestroyAPIView):
    """

        get:
        Return the details of a single seat object

        put:
        Updates a given seat object, non-partial update

        patch:
        Updates a given sear, partial update


        delete:
        Deletes a single object
        """

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class FlightTicketList(generics.ListAPIView):
    """A class view for listing all tickets booked for a particular flight"""

    permission_classes = (IsAdminUser,)
    serializer_class = TicketSerializer

    def get_queryset(self):
        flight = self.kwargs.get('flight')
        return Ticket.objects.filter(seat__flight=flight)


class TicketList(generics.ListAPIView):
    """A class view for listing all tickets"""

    permission_classes = (IsAdminUser,)
    filterset_class = TicketFilter
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    """

    get:
    Return the details of a single ticket

    put:
    Updates a given ticket, non-partial update

    patch:
    Updates a given ticket, partial update


    delete:
    Deletes a single ticket
    """

    permission_classes = (IsAdminUserOrOwnerReadOnly,)
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """

    get:
    Return the details of a single user

    put:
    Updates a given user, non-partial update

    patch:
    Updates a given user, partial update


    delete:
    Deletes a single user
    """

    permission_classes = (IsAdminUserOrOwnerReadAndUpdateOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    """A class view for getting a user list"""

    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
