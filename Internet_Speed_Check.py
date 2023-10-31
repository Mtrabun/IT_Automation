# Required libraries
import speedtest
import time


def check_speed():
    """Use the speedtest-cli library to check internet speed and return download, upload, and ping."""

    # Initialize a speedtest instance
    st = speedtest.Speedtest()

    # Get the best server based on ping to perform the speedtest
    st.get_best_server()

    # Retrieve and display server details to the user
    server = st.results.server
    print(f"Connected to server: {server['name']} in {server['cc']} sponsored by {server['sponsor']} with ID {server['id']}")

    # Ensuring that the test uses HTTPS for more accurate results
    st._secure = True

    # Get download speed, convert it from bits per second to Mbps and store it
    download_speed = st.download() / (10 ** 6)

    # Get upload speed, convert it from bits per second to Mbps and store it
    upload_speed = st.upload() / (10 ** 6)

    # Get the ping value
    ping_value = st.results.ping

    return download_speed, upload_speed, ping_value


def main():
    # Variables to store the cumulative speed values for later averaging
    total_download_speed = 0
    total_upload_speed = 0
    total_ping = 0

    # Set the number of checks to be conducted
    checks = 5

    # Define a variable for how many retries should be done if a speedtest fails
    retries = 3

    print("Starting internet speed check...\n")

    # Loop through the number of checks
    for i in range(checks):
        success = False  # Flag to keep track of a successful speed test

        # For each check, try up to the defined number of retries
        for _ in range(retries):
            try:
                print(f"Checking speed... {i + 1}/{checks}")
                download, upload, ping = check_speed()
                print(f"Download: {download:.2f} Mbps, Upload: {upload:.2f} Mbps, Ping: {ping} ms\n")

                # Add the results to the cumulative totals
                total_download_speed += download
                total_upload_speed += upload
                total_ping += ping
                success = True

                # If the check is successful, exit the retry loop
                break

            except Exception as e:  # Handle any exceptions raised during the speedtest
                print(f"An error occurred during check {i + 1} attempt {_ + 1}: {e}\n")
                if _ == retries - 1:  # If it's the last retry
                    checks -= 1  # Decrease the number of successful checks to adjust the average later

        # Pause for a minute before conducting the next check
        time.sleep(60)

    # Compute the average speed values across all checks
    avg_download = total_download_speed / checks
    avg_upload = total_upload_speed / checks
    avg_ping = total_ping / checks

    # Display the averaged results
    print("Average results over 5 checks:")
    print(f"Download: {avg_download:.2f} Mbps")
    print(f"Upload: {avg_upload:.2f} Mbps")
    print(f"Ping: {avg_ping:.2f} ms")


# This block ensures the script only runs when executed directly, and not when imported as a module
if __name__ == "__main__":
    main()
