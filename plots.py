from matplotlib import pyplot as plt

class Chart:
    def __init__(self):
        
        self.color = "#178905"
        plt.style.use("seaborn")

        pass


    def __UnpackDict__(self, data):
        """
        Takes values dictionary as input and returns
        list of lists as X and Y axis values for a chart
        """
        x_values = []
        y_values = []
        for item in data:
            x_values.append(item)
            y_values.append(data[item])
        return [x_values, y_values]    

    def Chart(
        self, data, label_X = "X axis", label_Y = "Y axis",
        title = "Chart", horizontal = False, pie_type = False
        ):
        """
        Generates chart out of presented data. If pie_type is True then pie chart is generated
        """

        values = self.__UnpackDict__(data)

        if pie_type:
            plt.pie(values[1], labels = values[0], shadow = True)
        else:
            if horizontal:
                plt.barh(values[0], values[1], color=self.color)
            else:
                plt.bar(values[0], values[1], color=self.color)
            plt.xlabel(label_X)
            plt.ylabel(label_Y)

        
        plt.title(title)

        plt.tight_layout()
        plt.show()
