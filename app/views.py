"""A module of app views"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.base_user import make_password, check_password
from requests.exceptions import HTTPError
from rest_framework import status, generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from social_django.utils import psa

from .models import User, Flight, Seat, Ticket
from .utils.enums import SeatStatus
from .serializers import (
    FlightSerializer,
    LoginSerializer,
    SeatSerializer,
    SocialSerializer,
    TicketSerializer,
    UserSerializer
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
    IsAdminUserOrOwnerReadAndUpdateOnly,
    IsAdminOrCreateOnly
)


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def welcome(request):
    return Response(template_name='app/welcome.html')


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data

        data = data.copy()
        img = data.get('image')
        data['image'] = upload_image(img) if img else ''

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(data.get('password'))
        serializer.validated_data['username'] = serializer.validated_data.get('email')
        del serializer.validated_data['confirm_password']
        serializer.save()

        payload = {
            'message': "Successfully signed up",
            'data': serializer.data
        }
        return Response(payload, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=data.get('email'))
        except ObjectDoesNotExist:
            return Response({'detail': "Wrong password or email"}, status=status.HTTP_400_BAD_REQUEST)
        if check_password(data.get('password'), user.password):
            token = generate_token(user)
            payload = {
                'message': "Successfully logged in",
                'token': token,
                'data': UserSerializer(user).data
            }
            payload['data']['isStaff'] = user.is_staff
            return Response(payload, status=status.HTTP_200_OK)
        return Response({'detail': 'Wrong password or email'}, status=status.HTTP_400_BAD_REQUEST)


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


class TicketList(generics.ListCreateAPIView):
    """A class view for listing all tickets"""

    permission_classes = (IsAuthenticated, IsAdminOrCreateOnly)
    filterset_class = TicketFilter
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(booked_by=self.request.user).order_by('id')

    def post(self, request):
        """
            Book flight ticket. Use the following test card details

            "pin": "1111",
            "number": "507850785078507812",
            "cvv": "081",
            "expiry_month": "12",
            "expiry_year":  "2020"
            """
        data = request.data
        serializer = TicketSerializer(data=data)
        serializer.is_valid(raise_exception=True)
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
            Ticket.objects.create(seat=seat, passenger=serializer.validated_data['passenger'],
                                  booked_by=request.user)
            update_seat_status(seat, SeatStatus.booked)

            flight_date = seat.flight.departure_date
            flight_time = seat.flight.departure_time
            flight_number = seat.flight.number
            seat_number = seat.seat_number
            mail_data = {
                'email': data.get('email'),
                'subject': 'Ticket Booking',
                'content': f'Ticket successfully booked\n date: {flight_date}\n time: {flight_time}\n flight no.: {flight_number}\n seat no.: {seat_number}'
            }

            send_email(mail_data)
            return Response({'message': 'Ticket successfully booked. Details have been sent by email'},
                            status=status.HTTP_200_OK)
        return Response({'detail': pay_resp['data']['message']}, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(http_method_names=['POST'])
@psa()
def exchange_token(request, backend):

    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user:
            return Response(
                {'errors': {'non_field_errors': "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.is_active:
            token = generate_token(user)
            payload = {
                'message': "Successfully logged in",
                'token': token,
                'data': UserSerializer(user).data
            }
            payload['data']['isStaff'] = user.is_staff
            return Response(payload, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': {'non_field_errors': 'This user account is inactive'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
