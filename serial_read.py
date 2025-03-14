import serial
import time
import os

def read_com_port_data(port_name, baud_rate, output_file):
    """
    Reads data from the specified COM port and outputs it in hexadecimal format to a file in the same directory as the script.
    The program ends after receiving one piece of data.
    :param port_name: COM port name, e.g., 'COM3'
    :param baud_rate: Baud rate
    :param output_file: Output file name
    """
    try:
        # Get the current working directory
        current_path = os.getcwd()
        print(f"Current working directory: {current_path}")

        output_path = os.path.join(current_path, output_file)
        ec_output_path = os.path.join(current_path, f"EC_{output_file}")

        # Open the serial port
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Successfully opened COM port {port_name}")

        # Open two output files (in append mode)
        with open(output_path, 'a') as file, open(ec_output_path, 'a') as ec_file:
            print(f"Data will be saved to: {output_path} and {ec_output_path}")
            print("Waiting to receive data...")

            while True:
                # Read data
                data = ser.read(4096)  # Read up to 4096 bytes at a time
                if data:
                    hex_data = data.hex()
                    print(f"Raw received data (hexadecimal): {hex_data}")

                    # Add the prefix '7e39700010' to the raw data
                    prefix = "7e39700010"
                    hex_data_with_prefix = prefix + hex_data
                    print(f"Data with prefix added: {hex_data_with_prefix}")

                    # Write the raw data to the EC_ prefixed file
                    ec_file.write(f"{hex_data_with_prefix}")
                    ec_file.flush()  # Immediately write data to disk

                    # Remove the first 18 characters and the last 4 characters
                    if len(hex_data_with_prefix) > 22:  # Ensure the data is long enough
                        hex_data_with_prefix = hex_data_with_prefix[18:-4]
                        print(f"Processed data: {hex_data_with_prefix}")

                        # Check and remove any unwanted prefixes (e.g., '100070f50f')
                        unwanted_prefix = "100070f50f"
                        if hex_data_with_prefix.startswith(unwanted_prefix):
                            hex_data_with_prefix = hex_data_with_prefix[len(unwanted_prefix):]
                            print(f"Data after removing unwanted prefix: {hex_data_with_prefix}")

                        # Write the data to the main file (without timestamp)
                        file.write(f"{hex_data_with_prefix}")
                        file.flush()  # Immediately write data to disk

                        print("Data has been saved, program will terminate.")
                        break

    except serial.SerialException as e:
        print(f"Error opening the COM port: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    # User input
    port_name = input("Please enter the COM port name (e.g., COM3): ")
    baud_rate = int(input("Please enter the baud rate (e.g., 9600): "))
    output_file = input("Please enter the name of the file to save data (e.g., data.txt): ")

    # Call the function to read data and save to a file
    read_com_port_data(port_name, baud_rate, output_file)