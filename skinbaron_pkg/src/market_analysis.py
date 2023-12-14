
import pandas as pd
import numpy as np


class ItemFilter:
    """
    A class to filter and merge data from two pandas DataFrames: 'newitems_df' and 'bestdeals_df'.
    merge the data and then filter the merged data based on various item attributes like name, rarity, exterior condition, and more.

    Attributes:
        newitems_df (DataFrame): DataFrame of new items.
        bestdeals_df (DataFrame): DataFrame of best deals.
    """

    def __init__(self, newitems_df, bestdeals_df):
        self.newitems_df = newitems_df
        self.bestdeals_df = bestdeals_df

    def filter_items(self, itemName=None, rarityName=None, exteriorName=None, variantTypeName=None, isSouvenir=None,
                     itemPrice=None, wear=None, isWearPrecise=None, stackable=None, tradeLockHoursLeft=None,
                     sticker_count=None, sticker_list=None):
        """
            Filters and merges two datasets, 'newitems_df' and 'bestdeals_df', based on various item attributes.

            This function performs an outer merge of two datasets based on 'salesId'
            and allows filtering based on item characteristics such as name, rarity, exterior, etc.
            It also processes sticker-related data.

            :param itemName (str, optional): Name of the item to filter.
            :param rarityName (str, optional): Rarity of the item to filter.
            :param exteriorName (str, optional): Exterior/condition of the item to filter.
            :param variantTypeName (str, optional): Type of the item variant to filter.
            :param isSouvenir (bool, optional): Whether the item is a souvenir.
            :param itemPrice (float, optional): Price of the item to filter.
            :param wear (float, optional): Wear value of the item to filter.
            :param isWearPrecise (bool, optional): Whether the wear value is precise.
            :param stackable (bool, optional): Whether the item is stackable.
            :param tradeLockHoursLeft (int, optional): Remaining trade lock hours on the item.
            :param sticker_count (int, optional): Number of stickers on the item.
            :param sticker_list (list, optional): List of specific stickers on the item.
            :return: A DataFrame after applying the specified filters.
            Example:
            ```
            item_filter = ItemFilter(newitems_df, bestdeals_df)
            1. no input params --> output the entire dataset with 100 new items listed and top 100 best deals
            and more features for buyers to learn:
            item_filter.filter_items()

            2. if buyers only want the item to be SG 553 | Bleached:
            item_filter.filter_items(itemName = 'SG 553 | Bleached')

            3. if buyers only want the item to be SG 553 | Bleached, and they want it has four stickers
            and two of the stickers should be 'Dust II (Gold)' and 'IEM (Gold) | Rio 2022'
            and they want the item to be factory new consumer grade:
            item_filter.filter_items(itemName = 'SG 553 | Bleached', rarityName= 'Consumer Grade', exteriorName= 'Factory New',
            sticker_count= 4, sticker_list= [' Dust II (Gold)', 'IEM (Gold) | Rio 2022'])

            4. specify all the params to find the item that match exactly:
            item_filter.filter_items(itemName = 'SG 553 | Bleached', rarityName= 'Consumer Grade', exteriorName= 'Factory New',
            variantTypeName='Rifle', isSouvenir=True, itemPrice=0.04, wear=5, isWearPrecise=True, stackable=False,
            tradeLockHoursLeft=6, sticker_count= 4, sticker_list= [' Dust II (Gold)', 'IEM (Gold) | Rio 2022'])
            ```
            """

        outer_merged_df = pd.merge(self.newitems_df, self.bestdeals_df, on=['salesId'], how='outer')
        common_columns = list(self.newitems_df.columns.intersection(self.bestdeals_df.columns))[1:]
        modified_list_x = [item + '_x' for item in common_columns]
        modified_list_y = [item + '_y' for item in common_columns]
        # for i in range(len(common_columns)):
        #     outer_merged_df[common_columns[i]] = outer_merged_df[modified_list_x[i]].combine_first(modified_list_y[i])
        #     outer_merged_df.drop(columns=[modified_list_x[i], modified_list_y[i]], inplace=True)
        for i in range(len(common_columns)):
            outer_merged_df[common_columns[i]] = outer_merged_df[modified_list_x[i]].combine_first(
                outer_merged_df[modified_list_y[i]])
            outer_merged_df.drop(columns=[modified_list_x[i], modified_list_y[i]], inplace=True)

        sticker_count_lst = list()
        localized_names = list()
        for i in range(outer_merged_df.shape[0]):
            try:
                sticker_count_lst.append(len(outer_merged_df.iloc[i]['stickers']))
                localized_names.append([sticker['localizedName'] for sticker in outer_merged_df.iloc[i]['stickers']])

            except Exception as e:
                sticker_count_lst.append(0)
                localized_names.append(None)
        outer_merged_df['sticker_count'] = sticker_count_lst
        outer_merged_df['sticker_list'] = localized_names

        if itemName != None:
            outer_merged_df = outer_merged_df[outer_merged_df['itemName'] == itemName]
        if rarityName != None:
            outer_merged_df = outer_merged_df[outer_merged_df['rarityName'] == rarityName]
        if exteriorName != None:
            outer_merged_df = outer_merged_df[outer_merged_df['exteriorName'] == exteriorName]
        if variantTypeName != None:
            outer_merged_df = outer_merged_df[outer_merged_df['variantTypeName'] == variantTypeName]
        if isSouvenir != None:
            outer_merged_df = outer_merged_df[outer_merged_df['isSouvenir'] == isSouvenir]
        if itemPrice != None:
            outer_merged_df = outer_merged_df[outer_merged_df['itemPrice'] == itemPrice]
        if wear != None:
            outer_merged_df['wear'] = np.around(outer_merged_df['wear'], decimals=0)
            outer_merged_df = outer_merged_df[outer_merged_df['wear'] == wear]
        if isWearPrecise != None:
            outer_merged_df = outer_merged_df[outer_merged_df['isWearPrecise'] == isWearPrecise]
        if stackable != None:
            outer_merged_df = outer_merged_df[outer_merged_df['stackable'] == stackable]
        if tradeLockHoursLeft != None:
            outer_merged_df['tradeLockHoursLeft'] = np.around(outer_merged_df['tradeLockHoursLeft'], decimals=0)
            outer_merged_df = outer_merged_df[outer_merged_df['tradeLockHoursLeft'] == tradeLockHoursLeft]
        if sticker_count != None:
            outer_merged_df = outer_merged_df[outer_merged_df['sticker_count'] == sticker_count]
        if sticker_list != None:
            outer_merged_df = outer_merged_df.dropna(subset=['sticker_list'])
            indices_to_drop = [i for i in range(outer_merged_df.shape[0]) if
                               not set(sticker_list).issubset(set(outer_merged_df.iloc[i]['sticker_list']))]
            outer_merged_df.drop(outer_merged_df.index[[indices_to_drop]], inplace=True)

        return outer_merged_df


