import logging

logging.basicConfig(
    filename='arena_tickets.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_ticket_index(tickets, ticket_id):
    for i, ticket in enumerate(tickets):
        if ticket.get("ticket_id") == ticket_id:
            return i
    return -1

def display_tickets(tickets):
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print("\n--- DANH SÁCH VÉ ---")
    print(f"{'Mã Vé':<5} | {'Tên Khách Hàng':<15} | {'Giá Vé':<7} | {'Chỗ Ngồi':<8} | Trạng Thái")
    print("-" * 59)

    for ticket in tickets:
        try:
            tid = ticket["ticket_id"]
            name = ticket["buyer_name"]
            price = ticket["price"]
            seat_zone, seat_num = ticket["seat"]
            status = ticket["status"]
            
            display_status = "Cancelled [ĐÃ HỦY]" if status == "Cancelled" else status
            seat_display = f"{seat_zone}-{seat_num}"
            
            print(f"{tid:<5} | {name:<15} | {price:<7} | {seat_display:<8} | {display_status}")
        except KeyError as e:
            print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
            logging.error(f"Missing key while displaying ticket: {e}")
            print("-" * 59)
            return

    print("-" * 59)
    logging.info("User viewed ticket list.")

def book_ticket(tickets):
    print("\n--- ĐẶT VÉ MỚI ---")
    
    ticket_id = input("Nhập mã vé: ").strip()
    if find_ticket_index(tickets, ticket_id) != -1:
        print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
        logging.warning(f"Duplicate ticket ID entered: {ticket_id}")
        return

    buyer_name = input("Nhập tên khách hàng: ").strip()

    while True:
        try:
            price_input = input("Nhập giá vé: ").strip()
            price = float(price_input)
            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")

    seat_zone = input("Nhập khu vực ghế: ").strip().upper()

    while True:
        try:
            seat_num = int(input("Nhập số ghế: ").strip())
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    new_ticket = {
        "ticket_id": ticket_id,
        "buyer_name": buyer_name,
        "price": price,
        "status": "Booked",
        "seat": (seat_zone, seat_num)
    }
    
    tickets.append(new_ticket)
    print(f"\nThành công: Đã đặt vé {ticket_id} cho khách hàng {buyer_name}.")
    logging.info(f"Booked new ticket {ticket_id} for {buyer_name}")

def change_seat(tickets):
    print("\n--- ĐỔI CHỖ NGỒI ---")
    ticket_id = input("Nhập mã vé cần đổi chỗ: ").strip()
    
    index = find_ticket_index(tickets, ticket_id)
    if index == -1:
        print(f"\nKhông tìm thấy vé mang mã {ticket_id}.")
        logging.warning(f"Change seat failed - Ticket {ticket_id} not found")
        return

    new_zone = input("Nhập khu vực ghế mới: ").strip().upper()
    
    while True:
        try:
            new_num = int(input("Nhập số ghế mới: ").strip())
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    tickets[index]["seat"] = (new_zone, new_num)
    
    print(f"\nThành công: Đã đổi chỗ vé {ticket_id} sang {new_zone}-{new_num}.")
    logging.info(f"Seat changed for ticket {ticket_id} to {new_zone}-{new_num}")

def cancel_ticket(tickets):
    print("\n--- HỦY VÉ ---")
    ticket_id = input("Nhập mã vé cần hủy: ").strip()
    
    index = find_ticket_index(tickets, ticket_id)
    if index == -1:
        print(f"\nKhông tìm thấy vé mang mã {ticket_id}.")
        logging.warning(f"Cancel ticket failed - Ticket {ticket_id} not found")
        return

    if tickets[index]["status"] == "Cancelled":
        print(f"\nVé {ticket_id} đã ở trạng thái Cancelled trước đó.")
        return

    tickets[index]["status"] = "Cancelled"
    print(f"\nThành công: Vé {ticket_id} đã được hủy.")
    logging.warning(f"Ticket {ticket_id} has been cancelled.")

def calculate_total_revenue(tickets):
    revenue = 0.0
    for ticket in tickets:
        if ticket["status"] == "Booked":
            revenue += ticket["price"]
    return revenue

def generate_revenue_report(tickets):
    print("\n--- BÁO CÁO DOANH THU ---")
    
    booked_count = 0
    cancelled_count = 0
    
    try:
        for ticket in tickets:
            if ticket["status"] == "Booked":
                booked_count += 1
            elif ticket["status"] == "Cancelled":
                cancelled_count += 1
                
        total_revenue = calculate_total_revenue(tickets)
        
    except KeyError as e:
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
        logging.error(f"Missing key while calculating revenue: {e}")
        print(f"Tổng doanh thu hợp lệ: 0.0")
        return

    print(f"Tổng số vé đã đặt: {booked_count}")
    print(f"Tổng số vé đã hủy: {cancelled_count}")
    print(f"Tổng doanh thu hợp lệ: {total_revenue:,.1f}")
    logging.info(f"Revenue report generated. Total: {total_revenue}")

if __name__ == "__main__":
    ticket_db = [
        {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
        {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
        {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
    ]

    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
        print("1. Xem danh sách vé đã bán")
        print("2. Đặt vé mới")
        print("3. Đổi chỗ ngồi (Cập nhật vé)")
        print("4. Hủy vé")
        print("5. Báo cáo doanh thu")
        print("6. Thoát chương trình")
        print("========================================")
        
        choice = input("Chọn chức năng (1-6): ").strip()
        
        match choice:
            case "1":
                display_tickets(ticket_db)
            case "2":
                book_ticket(ticket_db)
            case "3":
                change_seat(ticket_db)
            case "4":
                cancel_ticket(ticket_db)
            case "5":
                generate_revenue_report(ticket_db)
            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
                logging.info("Ticket management system closed.")
                break
            case _:
                print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-6.")