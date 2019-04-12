"""A module of app views"""
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.base_user import make_password, check_password
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, FlightSerializer, SeatSerializer, TicketSerializer
from .models import User, Flight, Seat, Ticket
from .utils.enums import SeatStatus, PaymentStatus
from .utils.helpers import(
    generate_token,
    upload_image,
    send_email,
    make_payment,
    update_seat_status,
    IsAdminUserOrReadOnly,
    IsAdminUserOrOwnerReadOnly,
    IsAdminUserOrOwnerReadAndUpdateOnly
)


@api_view(['GET'])
def welcome(request):
    return render(request, 'app/welcome.html')


@api_view(['POST'])
def user_signup(request):
    """Endpoint to register a user"""
    data = request.data

    if data['password'] == data['confirm_password']:
        data = data.copy()
        img = data['image']
        data['image'] = upload_image(img)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(data['password'])
            serializer.validated_data['username'] = serializer.validated_data['email']
            serializer.save()

            user = get_object_or_404(User, email=data['email'])
            token = generate_token(user)
            payload = {
                        'token': token,
                        'message': "Successfully signed up",
                        'user': serializer.data
                        }
            return Response(payload, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_signin(request):
    """Endpoint for user login"""
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    if check_password(data['password'], user.password):
        token = generate_token(user)
        payload = {
                    'token': token,
                    'message': "Successfully logged in",
                }
        return Response(payload, status=status.HTTP_200_OK)
    return Response({'message': 'Wrong password or email'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def make_reservation(request):
    """Endpoint to make flight reservation"""
    data = request.data
    data = data.copy()
    if not data['email']:
        data['email'] = request.user.email
    serializer = TicketSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['payment_status'] = PaymentStatus.pending
        serializer.validated_data['booked_by'] = request.user
        seat = serializer.validated_data['seat']
        flight_date = datetime.strftime(seat.flight.departure_time, '%Y-%m-%d %H:%M')
        flight_number = seat.flight.number
        seat_number = seat.seat_number
        serializer.save()
        update_seat_status(seat, SeatStatus.booked)

        mail_data = {
            'email': data.get('email', request.user.email),
            'subject': 'Ticket Reservation',
            'content': f'Reservation made\nPassenger: {data["passenger"]} \ndate: {flight_date}\n flight no.: {flight_number}\n seat no.: {seat_number}'
        }
        send_email(mail_data)
        return Response({'message': 'Reservation successful. Details have been sent by email'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def payment(request):
    """Endpoint to enable online payment using Paystack"""
    data = request.data
    payment_data = {
        "email": data['email'],
        "amount": data['amount'],
        "pin": data['pin'],
        "card": {
            "number": data['number'],
            "cvv": data['cvv'],
            "expiry_month": data['expiry_month'],
            "expiry_year":  data['expiry_year']
        }
    }
    pay_resp = make_payment(payment_data)
    if pay_resp['data']['status'] != 'success':
        return Response({'message': pay_resp.data.display_text}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def book_ticket(request):
    """Book flight ticket"""
    data = request.data
    serializer = TicketSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['booked_by'] = request.user
        seat = serializer.validated_data['seat']
        payment_data = {
            'email': data.get('email', request.user.email),
            "amount": str(seat.flight.fare),
            "pin": data['pin'],
            "card": {
                "number": data['number'],
                "cvv": data['cvv'],
                "expiry_month": data['expiry_month'],
                "expiry_year": data['expiry_year']
            }
        }
        pay_resp = make_payment(payment_data)

        if pay_resp['data']['status'] == 'success':
            serializer.validated_data['booked_by'] = request.user
            serializer.save()
            update_seat_status(seat, SeatStatus.booked)

            flight_date = datetime.strftime(seat.flight.departure_time, '%Y-%m-%d %H:%M')
            flight_number = seat.flight.number
            seat_number = seat.seat_number
            mail_data = {
                'email': data['email'],
                'subject': 'Ticket Booking',
                'content': f'Ticket successfully booked\n date: {flight_date}\n flight no.: {flight_number}\n seat no.: {seat_number}'
            }

            send_email(mail_data)
            return Response({'message': 'Ticket successfully booked. Details have been sent by email'}, status=status.HTTP_200_OK)
        return Response({'message': pay_resp.data.display_text}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class TicketList(generics.ListAPIView):
    """A class view for listing all tickets booked for a particular flight"""

    permission_classes = (IsAdminUser,)
    serializer_class = TicketSerializer

    def get_queryset(self):
        flight = self.kwargs['flight']
        return Ticket.objects.filter(seat__flight=flight)


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

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
