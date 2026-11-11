
import pandas as pd


def validate_gps_data(data):

    required_columns = [
        "DeviceID",
        "Lat",
        "Long",
        "Timestamp"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df = data.copy()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    results = {
        "total_records": len(df),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_records": int(df.duplicated().sum()),
        "invalid_latitude": int(
            (~df["Lat"].between(-90, 90)).sum()
        ),
        "invalid_longitude": int(
            (~df["Long"].between(-180, 180)).sum()
        ),
        "invalid_timestamps": int(
            df["Timestamp"].isna().sum()
        ),
        "unique_devices": int(
            df["DeviceID"].nunique()
        )
    }

    return results


if __name__ == "__main__":

    gps_data = pd.read_csv(
        "data/raw/gps_pings.csv"
    )

    report = validate_gps_data(gps_data)

    print("\nGEO PULSE DATA VALIDATION REPORT")
    print("=" * 40)

    for key, value in report.items():
        print(f"{key}: {value}")

