import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


def clean():

    df = pd.read_csv("assets\immoweb_properties_data2.csv")

    df = df[df["url"].str.contains("new-real-estate-project") == False]

    df.rename(
        columns={
            "Living area": "area",
            "Address": "full_address",
            "Garden surface": "garden_area",
            "Terrace surface": "terrace_area",
            "Garden": "garden",
            "Garden surface": "garden_area",
            "Swimming pool": "swimming_pool",
            "Kitchen type": "equipped_kitchen",
            "Furnished": "furnished",
            "How many fireplaces?": "open_fire",
            "Terrace": "terrace",
            "Number of frontages": "facades_number",
            "Building condition": "building_state",
            "Bedrooms": "rooms_number",
            "Surface of the plot": "land_area",
            "Price": "price",
        },
        inplace=True,
    )
    df["zip_code"] = df["url"].str.extract(r"([0-9]{1,5})").astype(int)
    df["property_type"] = df["url"].str.split("/").str[5]
    df['property_type'] = df['property_type'].apply(lambda x: 'HOUSE' if x in ['house', 'villa', 'mansion', 'manor-house', 'country-cottage', 'town-house', 'chalet', 'farmhouse'] else ('APARTMENT' if x in ['apartment', 'loft', 'flat-studio', 'duplex', 'service-flat', 'apartment-block', 'triplex', 'penthouse', 'ground-floor', 'kot'] else 'OTHERS'))
    df['property_type'] = df['property_type'].replace('HOUSE',2,regex=True)
    df['property_type'] = df['property_type'].replace('APARTMENT',1,regex=True)
    df['property_type'] = df['property_type'].replace('OTHERS',0,regex=True)

    df = df[
        [
            "area",
            "property_type",
            "price",
            "rooms_number",
            "zip_code",
            "land_area",
            "garden",
            "garden_area",
            "equipped_kitchen",
            "full_address",
            "swimming_pool",
            "furnished",
            "open_fire",
            "terrace",
            "terrace_area",
            "facades_number",
            "building_state"
        ]
    ]


    df["terrace"] = df["terrace"].replace({"Yes": 1, "No": 0}).fillna(0)
    df["terrace_area"] = df["terrace_area"].str.extract(r"([0-9]{1,3})").astype(float)
    df["area"] = df["area"].str.extract(r"([0-9]{2,5})").astype(float)
    df["garden"] = df["garden"].replace({"Yes": 1, "No": 0}).fillna(0)
    df["garden_area"] = df["garden_area"].str.extract(r"([0-9]{2,5})").astype(float)
    df["land_area"] = df["land_area"].str.extract(r"([0-9]{1,7})").astype(float)
    df["swimming_pool"] = df["swimming_pool"].replace(["Yes", "No"], [1, 0]).fillna(0)
    df["furnished"] = df["furnished"].replace(["Yes", "No"], [1, 0]).fillna(0)
    df["open_fire"] = df["open_fire"].replace(1.0, 1).fillna(0) 
    df["price"] = df["price"].str.extract(r"([0-9]{4,7})").astype(float)
    kitchen_type_scale={'USA hyper equipped':1, 'USA installed':1, 'USA semi equipped':1, 'USA uninstalled':0, 
                        'Hyper equipped':1, 'Installed':1, 'Semi equipped':1, 'Not installed':0}
    df['equipped_kitchen'] = df['equipped_kitchen'].map(kitchen_type_scale)
    building_condition_scale={'As new':5,'Just renovated':4, 'Good':3, 'To renovate':2, 
                                'To restore':1, 'To be done up':1}
    df['building_state'] = df['building_state'].map(building_condition_scale)    
    df["price"].replace("", np.nan, inplace=True)
    df["building_state"].replace("", np.nan, inplace=True)
    df["full_address"].replace("", np.nan, inplace=True)
    df["area"].replace("", np.nan, inplace=True)
    df.dropna(subset=["price", "full_address", "area", "rooms_number","property_type","building_state"], inplace=True)

    imputer = SimpleImputer(strategy='mean', missing_values=np.nan)
    imputed_columns = ['terrace_area', 'garden_area', 'land_area',
                                        'facades_number', 'equipped_kitchen', 'building_state']
    imputer = imputer.fit(df[imputed_columns])
    df[imputed_columns] = imputer.transform(df[imputed_columns])
    df=df.drop_duplicates()

    print(df.isnull().sum())

    def subset_by_iqr(df, column, whisker_width=1.5):
        """Remove outliers from a dataframe by column, including optional whiskers, removing rows for which the column 
        value are less than Q1-1.5IQR or greater than Q3+1.5IQR.
        Args: df (`:obj:pd.DataFrame`): A pandas dataframe to subset 
        column (str): Name of the column to calculate the subset from.
        whisker_width (float): Optional, loosen the IQR filter by a factor of `whisker_width` * IQR.
        Returns:
            (`:obj:pd.DataFrame`): Filtered dataframe
        """
        # Calculate Q1, Q2 and IQR
        q1 = df[column].quantile(0.25)                 
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        # Apply filter with respect to IQR, including optional whiskers
        filter = (df[column] >= q1 - whisker_width*iqr) & (df[column] <= q3 + whisker_width*iqr)
        return df.loc[filter]

    outlier_list = ['area', 'price', 'rooms_number']
    for variable in outlier_list:
        df = subset_by_iqr(df, variable, whisker_width=1.5)

    print(df.shape)

    df.to_csv("assets\\test.csv")

clean()