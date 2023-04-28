import snipe_sofa_framework

ids = ["2227"]

print(len(ids))

payload = {
    "model_id": "680",
    "_snipeit_display_size_7": '13"',
    "_snipeit_cpu_family_8": "Intel",
    "_snipeit_cpu_type_9": "",
    "_snipeit_cpu_core_10": "",
    "_snipeit_gpu_family_11": "Intel",
    "_snipeit_gpu_type_12": "Iris",
    "_snipeit_gpu_core_13": "",
    "_snipeit_ram_14":  "",
    "_snipeit_storage_15":  "",
    "_snipeit_touchscreen_16":  "",
    "_snipeit_keyboard_layout_17":  "",
    "_snipeit_model_year_18":   "",
    "_snipeit_color_19":    ""
}

for asset_id in ids:
    snipe_sofa_framework.Snipe().update_asset_model_data(asset_id=asset_id, payload=payload)
