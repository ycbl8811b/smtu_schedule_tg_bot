import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import datetime
from PIL import Image

from utils.validation.db_validation import validated_time



class TableManager:
    def __init__(self):
        self.__HEADER_HEIGHT = 0.03
        self.__COLUMNS_WIDTH = {
            0: 0.03,
            1: 0.03,
            2: 0.07,
            3: 0.08,
            4: 0.04,
            6: 0.025
        }
    

    def __adjust_cells_props(self, table, df):
        def __adjust_height(cell):
            if row_id == 0:
                cell.set_height(self.__HEADER_HEIGHT)
            else:
                cell.set_height(self.__row_height)
        
        def __adjust_width(cell):
            try:
                cell.set_width(self.__COLUMNS_WIDTH[column_id])
            except KeyError:
                pass
        
        def __adjust_text_props(cell):
            cell.set_text_props(visible=True)
            if row_id > 0 and column_id == 6:
                cell.set_text_props(visible=False)


        for row_id in range(len(df.index)+1):
            for column_id in range(len(df.columns)):
                cell = table[row_id, column_id]
                __adjust_height(cell)
                __adjust_width(cell)
                __adjust_text_props(cell)


    def __formatted_columns_data(self, rows):
            columns = []
            for i in range(len(rows[0])):
                column = []
                for j in range(len(rows)):
                    column.append(rows[j][i])
                columns.append(column)
            
            return columns
    

    def __create_dataframe(self, columns_names, rows):
            columns_data = self.__formatted_columns_data(rows)
            table = {}
            for i in range(len(columns_names)):
                table[columns_names[i]] = columns_data[i]

            return pd.DataFrame(table)
    

    def __create_subplots(self):
        fig, ax = plt.subplots(figsize=(8,4))
        return fig, ax
    

    def __adjust_ax(self, ax, *args):
        for arg in args:
            ax.axis(arg)


    def __create_table(self, df, ax):
        def __get_bbox_height():
            if self.__row_height == 0.125:
                return 0.125*len(df.index) + self.__HEADER_HEIGHT
            return 1
        
        self.__adjust_ax(ax, "tight", "off")

        bbox_height = __get_bbox_height()
        return ax.table(cellText=df.values, colLabels=df.columns,
                    cellLoc="center", loc="center",
                    bbox=[0,0,1,bbox_height])


    def __adjust_table_font(self, table, fontsize):
            table.auto_set_font_size(False)
            table.set_fontsize(fontsize)


    def __calc_row_height(self, df):
        height = (1 - self.__HEADER_HEIGHT) / len(df.index)
        if height > 0.125:
            return 0.125
        return height


    def __set_row_height(self, height):
        self.__row_height = height
    

    def render_table(self, columns_names, rows):
        def __render_images(table, ax, df):
            def __get_inset_axes():
                def __get_axes_margin():
                    left_margin = 0.7225
                    bottom_margin = (self.__row_height - __get_image_height())/2 + (self.__row_height * (row_id-1))
                    return (left_margin, bottom_margin)

                def __get_image_height():
                    if 0.8*self.__row_height > 0.115:
                        return 0.115
                    return 0.8*self.__row_height

                img_width = 0.0325
                img_height = __get_image_height()
                left_margin, bottom_margin = __get_axes_margin()
                return (left_margin, bottom_margin, img_width, img_height)
            

            def __get_image_path():
                return "/home/user/projects/schedule_bot/assets/"+ df["Фото"][len(df)+1 - row_id-1]
            
            
            for row_id in range(1, len(df)+1):
                image_path = __get_image_path()
                if "no image" not in image_path:
                    img = Image.open(image_path)
                    inset_axes = __get_inset_axes()
                    ax_img = ax.inset_axes([*inset_axes])
                    ax_img.imshow(img)
                    self.__adjust_ax(ax_img, "tight", "off")
    

        df = self.__create_dataframe(columns_names, rows)
        height = self.__calc_row_height(df)
        self.__set_row_height(height)
        fig, ax = self.__create_subplots()
        table = self.__create_table(df, ax)
        self.__adjust_table_font(table, 4)        
        self.__adjust_cells_props(table, df)

        __render_images(table, ax, df)
        path = "assets/tables/table.png"
        plt.savefig(path, dpi=600, bbox_inches="tight")
        return path
