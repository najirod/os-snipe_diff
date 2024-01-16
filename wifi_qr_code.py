import qrcode

# Define WiFi network parameters
ssid = "SofaIT-test_4"
ssid = "sofa"
auth_type = "WPA2-EAP"
eap_method = "PEAP" #"PEAP"
phase_2_method = "MSCHAPV2"
username = "marko"
password = "konj"
hidden = False  # Set to "true" if the network is hidden; otherwise, use "false"

# Create a WiFi configuration string with both username and password
wifi_config ="WIFI:S:SofaIT-test_4;T:WPA2-EAP;E:PEAP;I:marko;PH2:MSCHAPV2;P:zg2012ss;;"# f"WIFI:T:WPA2-EAP;:S:{ssid};E:{eap_method};PH2:{phase_2_method};A:marko;I:{username};P:{password};;"#f"WIFI:T:{auth_type};S:{ssid};P:'konj';H:false;E:{eap_method};A:marko;;" #f"WIFI:T:WPA2-EAP;S:{ssid};I:{username};P:{password};PH2:MSCHAPV2;E:{eap_method};H:false"
#tspheaiph2
#WIFI:S:sofa;T:WPA2-EAP;P:passs;E:PEAP;PH2:MSCHAPV2;I:marko;;
# f"WIFI:T:{auth_type};S:{ssid};P:{password};H:{hidden};;"
# f"WIFI:T:WPA2-EAP;S:{ssid};E:{eap_method};PH2:{phase_2_method};I:{username};P:{password};;"
# Generate the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wifi_config)
qr.make(fit=True)

# Create the QR code image
qr_code = qr.make_image(fill_color="green", back_color="white")

# Save the QR code as an image
qr_code.save("wifi_qr_code.png")

print("QR code saved as wifi_qr_code.png")
