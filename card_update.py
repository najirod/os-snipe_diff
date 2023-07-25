import snipe_sofa_framework

user_id = "155"

assets = snipe_sofa_framework.Snipe().get_checked_out_assets_by_id(user_id=user_id)
for asset_tag in assets:
    if assets[asset_tag]["model"] == "Kartica za ulazak u firmu":
        print(assets[asset_tag])

# snipe_sofa_framework.Update("01696").set_card_hex("92164cd6")
print(snipe_sofa_framework.Snipe().statement_user_data())
