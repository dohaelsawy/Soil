from django.test import TestCase
from .models import Space


class SpacesViewTest(TestCase) :

    @classmethod
    def setUpTestData(cls):
        Space.objects.create(
            name="room1",
            type='private_office',
            capacity=30,
            price_per_hour=100,
            availability=True
        )

        Space.objects.create(
            name="room2",
            type='private_office',
            capacity=30,
            price_per_hour=100,
            availability=False
        )


    def test_create_space_success(self):
        response = self.client.post(
            path='/spaces/',
            data={
                "name": "room3",
                "type": "meeting_room",
                "capacity": 32,
                "price_per_hour": 322.00,
                "availability": False
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code,201)

        response_data = response.json()
        self.assertEqual(response_data['name'],"room3")
        self.assertEqual(response_data['type'],"meeting_room")
        self.assertEqual(response_data['capacity'],32)
        self.assertEqual(response_data['price_per_hour'],'322.00')
        self.assertEqual(response_data['availability'],False)



    def test_create_non_unique_space(self):
        response = self.client.post(
            path='/spaces/',
            data={
                "name": "room1",
                "type": "meeting_room",
                "capacity": 32,
                "price_per_hour": "322.00",
                "availability": False
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)

        response_data = response.json()
        self.assertEqual(response_data['errors']['name'],['space with this name already exists.'])

        


    def test_create_negative_capacity_price_space(self):
        response = self.client.post(
            path='/spaces/',
            data={
                "name": "room3",
                "type": "meeting_room",
                "capacity": -32,
                "price_per_hour": "-322.00",
                "availability": False
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,400)

        response_data = response.json()
        self.assertEqual(response_data['errors']['capacity'],["Ensure this value is greater than or equal to 0."])
        self.assertEqual(response_data['errors']['price_per_hour'],["Price cannot be negative."])




    def test_update_space_success(self):
        response = self.client.patch(
            path='/spaces/1/',
            data={
                "type": "private_office",
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code,200)
        
        response_data = response.json()
        self.assertEqual(response_data['type'],"private_office")




    def test_available_spaces_success(self):
        response = self.client.get(
            path='/spaces/available_spaces/',
        )
        self.assertEqual(response.status_code,200)

        response_data = response.json()
        self.assertEqual(len(response_data),1)
        self.assertEqual(response_data[0]['id'],1)


    def test_delete_existed_space_success(self):
        response = self.client.delete(
            path='/spaces/1/',
        )
        print(response.content)
        self.assertEqual(response.status_code,200)
        response_data = response.json()
        self.assertEqual(response_data['message'],"Space deleted successfully.")



    def test_delete_non_existed_space_error(self):
        response = self.client.delete(
            path='/spaces/3/',
        )
        self.assertEqual(response.status_code,400)

        response_data = response.json()
        self.assertEqual(response_data['error'],"The requested Space does not exist.")

    
    def test_get_non_existed_space_error(self):
        response = self.client.get(
            path='/spaces/10/',
        )
        self.assertEqual(response.status_code,400)

        response_data = response.json()
        self.assertEqual(response_data['error'],"The requested Space does not exist.")

