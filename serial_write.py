import serial
import sys

def write_to_com_port(port_name, baud_rate, file_path):
    """
    Write the hexadecimal content from the specified file to the specified COM port.
    :param port_name: COM port name, e.g. 'COM3'
    :param baud_rate: Baud rate
    :param file_path: Path to the file containing hexadecimal data
    """
    try:
        # Remove surrounding quotes from the file path (if any)
        file_path = file_path.strip('"')

        # Read the file content
        with open(file_path, 'r') as file:
            data_hex = file.read().strip()
        
        # Convert the hexadecimal string to byte data
        data_bytes = bytes.fromhex(data_hex)
        
        # Open the serial port
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Successfully opened COM port {port_name}")

        # Write the data to the COM port
        ser.write(data_bytes)
        print(f"Written {len(data_bytes)} bytes to {port_name}")
        
        # Print debug information: display data in hexadecimal format
        print(f"Data sent (hex): {data_bytes.hex()}")
    
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except ValueError as e:
        print(f"Hexadecimal data format error: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()  # Ensure the serial port is closed
            print("Serial port closed.")

if __name__ == "__main__":
    port_name = input("Enter the COM port name (e.g., COM3): ")
    baud_rate = int(input("Enter the baud rate (e.g., 9600): "))
    file_path = input(r"Enter the file path containing hexadecimal data (e.g., C:\Users\HP-9CG47702N9\Desktop\EC_TotalLength4096Chars.txt): ")  # Raw string here
    
    # Call the function to write data
    write_to_com_port(port_name, baud_rate, file_path)
    
    # Keep the program running until the user presses a key
    input("Program completed. Press any key to exit...")  # Wait for user input to avoid immediate exit