import unittest
from main import calculate_total_revenue

class TestTicketingRevenue(unittest.TestCase):
    
    def test_mixed_tickets_revenue(self):
        mock_tickets = [
            {"ticket_id": "T01", "price": 500.0, "status": "Booked"},
            {"ticket_id": "T02", "price": 300.0, "status": "Cancelled"},
            {"ticket_id": "T03", "price": 500.0, "status": "Booked"}
        ]
        
        result = calculate_total_revenue(mock_tickets)
        self.assertEqual(result, 1000.0)

    def test_empty_ticket_list(self):
        empty_tickets = []
        
        result = calculate_total_revenue(empty_tickets)
        self.assertEqual(result, 0.0)

if __name__ == '__main__':
    unittest.main()