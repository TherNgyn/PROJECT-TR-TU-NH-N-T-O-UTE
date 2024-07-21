import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
from tkinter import messagebox
from logpy import run, fact, eq, Relation, var


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.adjacent = Relation()
        self.coastal = Relation()

        self.file_coastal = 'coastal_states.txt'
        self.file_adjacent = 'adjacent_states.txt'

        # Read the file containing the coastal states
        with open(self.file_coastal, 'r') as f:
            line = f.read()
            coastal_states = line.split(',')

        # Add the info to the fact base
        for state in coastal_states:
            fact(self.coastal, state)

        # Read the file containing the coastal states
        with open(self.file_adjacent, 'r') as f:
            adjlist = [line.strip().split(',') for line in f if line and line[0].isalpha()]

        # Add the info to the fact base
        for L in adjlist:
            head, tail = L[0], L[1:]
            for state in tail:
                fact(self.adjacent, head, state)

        # Initialize the variables
        self.x = var()

        self.title('Analyzing Geography')
        self.cvs_map = tk.Canvas(self, width=620, height=480, relief = tk.SUNKEN, border = 2)
        self.ve_ban_do([])
        lbl_frm_menu = tk.LabelFrame(self, text = 'Menu', width = 300, height = 100)
        self.lbl_frm_menu_2 = tk.LabelFrame(self, text = 'The result board', width = 300, height = 100)
        self.lst_city = ["Alabama", "Arizona", "Arkansas",
            "California", "Colorado", "Connecticut", "Delaware",
            "Florida", "Georgia", "Idaho", "Illinois", "Indiana",
            "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
            "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
            "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
            "North Dakota", "Ohio", "Oklahoma", "Oregon",
            "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
            "Washington", "West Virginia", "Wisconsin", "Wyoming"]

        self.notebook = ttk.Notebook(self.lbl_frm_menu_2)
        self.tab_bang_ke = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bang_ke, text = 'Adjacent States')
        self.tab_ke_ven_bien = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ke_ven_bien, text = 'Coastal States \nAdjacent')
        self.tab_ke_2_bang = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ke_2_bang, text = 'States that border \nthe two chosen states')
        self.notebook.grid(row = 0, column = 0, padx=5, pady=7, sticky = tk.EW)

        self.text_widget_1 = tk.Text(self.tab_bang_ke , width = 35, height = 15)
        self.text_widget_1.tag_configure('center', justify='center', font=('Georgia', 12))
        self.text_widget_1.grid(row=0, column=0, padx=5, pady=5, sticky = tk.EW)
        self.text_widget_2 = tk.Text(self.tab_ke_ven_bien , width = 35, height = 15)
        self.text_widget_2.tag_configure('center', justify='center', font=('Georgia', 12))
        self.text_widget_2.grid(row=0, column=0, padx=5, pady=5, sticky = tk.EW)
        self.text_widget_3 = tk.Text(self.tab_ke_2_bang , width = 35, height = 15)
        self.text_widget_3.tag_configure('center', justify='center', font=('Georgia', 12))
        self.text_widget_3.grid(row=0, column=0, padx=5, pady=5, sticky = tk.EW)

        btn_click_bang_ke = ttk.Button(lbl_frm_menu, text = 'Adjacent States', command= self.btn_bang_ke_click)
        btn_click_ke_ven_bien = ttk.Button(lbl_frm_menu, text = 'Coastal States Adjacent', command= self.btn_ke_ven_bien_click)
        btn_click_ke_2_bang = ttk.Button(lbl_frm_menu, text = 'States that border the two chosen states',command= self.btn_ke_2_bang_click)

        lbl_chon_bang = ttk.Label(lbl_frm_menu, text = 'Select State')
        self.cbo_chon_bang = ttk.Combobox(lbl_frm_menu, value = self.lst_city)
        self.cbo_chon_bang.set('')
        self.cbo_chon_bang.bind("<<ComboboxSelected>>", self.cbo_chon_bang_click)
        lbl_chon_bang.grid(row=0, column=0, padx = 5, pady = 0, sticky = tk.W)
        self.cbo_chon_bang.grid(row=1, column=0, padx = 5, pady = 5, sticky = tk.EW)

        lbl_ke_2_bang = ttk.Label(lbl_frm_menu, text = 'Select The Second State')
        self.cbo_ke_2_bang = ttk.Combobox(lbl_frm_menu, value = self.lst_city)
        self.cbo_ke_2_bang.set('')
        self.cbo_ke_2_bang.bind("<<ComboboxSelected>>", self.cbo_ke_2_bang_click)
        lbl_ke_2_bang.grid(row=6, column=0, padx = 5, pady = 0, sticky = tk.W)
        self.cbo_ke_2_bang.grid(row=7, column=0, padx = 5, pady = 5, sticky = tk.EW)

        btn_click_bang_ke.grid(row=4, column=0, padx=5, pady=5, sticky = tk.EW)
        btn_click_ke_ven_bien.grid(row=5, column=0, padx=5, pady=5, sticky = tk.EW)
        btn_click_ke_2_bang.grid(row=8, column=0, padx=5, pady=5, sticky = tk.EW)

        self.cvs_map.grid(row=0, column=0, padx =5, pady = 5)
        lbl_frm_menu.grid(row = 0, column=1, padx=5, pady=7, sticky = tk.N)
        self.lbl_frm_menu_2.grid(row = 0, column = 1 , padx=5, pady=7, sticky = tk.EW)

    def ve_ban_do(self, states_to_fill):
        state_coords = {
            'California': (-119.4179, 36.7783),
            'Texas': (-99.9018, 31.9686),
            'Florida': (-81.5158, 27.6648),
            'New York': (-75.3060, 42.7128),
            'Illinois': (-89.3985, 40.6331),
            'Pennsylvania': (-77.4945, 40.9033),
            'Ohio': (-82.9071, 40.4173),
            'Georgia': (-83.5389, 32.1656),
            'North Carolina': (-79.0193, 35.4596),
            'Michigan': (-84.5068, 43.1148),
            '6': (-74.4057, 40.0583),
            'Virginia': (-78.2494, 37.5407),
            'Washington': (-120.3321, 46.8062),
            'Arizona': (-111.2937, 34.4484),
            '3': (-71.4589, 42.3601),
            'Tennessee': (-86.7816, 35.8627),
            'Indiana': (-86.1349, 39.7684),
            'Missouri': (-92.3295, 38.5767),
            '8': (-76.7413, 39.0458),
            'Wisconsin': (-89.4012, 44.2731),
            'Colorado': (-105.9821, 39.2501),
            'Minnesota': (-94.4650, 46.0778),
            'South Carolina': (-81.1637, 33.8361),
            'Alabama': (-86.6023, 33.3182),
            'Louisiana': (-91.8749, 30.0843),
            'Kentucky': (-84.7700, 37.4393),
            'Oregon': (-120.6765, 43.8393),
            'Oklahoma': (-97.0929, 35.0078),
            '5': (-73.0877, 41.6032),
            'Iowa': (-93.6977, 41.8780),
            'Mississippi': (-89.4985, 32.3547),
            'Arkansas': (-92.3311, 34.7465),
            'Utah': (-111.8535, 39.5608),
            'Nevada': (-116.4398, 39.1699),
            'Kansas': (-98.4842, 38.4119),
            'New Mexico': (-105.6056, 34.5199),
            'Nebraska': (-99.9018, 41.4925),
            '9': (-80.7549, 38.3498),
            'Idaho': (-114.7420, 44.0682),
            'Maine': (-69.0455, 45.2538),
            '1': (-71.5724, 43.1939),
            '4': (-71.4828, 41.5801),
            'Montana': (-109.3626, 46.8797),
            '7': (-75.5277, 38.9108),
            'South Dakota': (-99.9018, 44.3683),
            'North Dakota': (-100.7837, 47.5515),
            '2': (-72.6778, 44.1588),
            'Wyoming': (-107.2903, 43.0760)
        }
        states_digit = {'1': 'New Hamsphire', '2': 'Vermont', '3': 'Massachusetts', '4': 'Rhode Island',
                        '5': 'Connecticut', '6': 'New Jersey', '7': 'Delaware', '8': 'Maryland', 
                         '9': 'West Virginia'}
        
        fig = plt.figure(figsize=(10,8))  # Tạo một figure
        ax = fig.add_subplot(1,1,1)  # Tạo một subplot

        m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95, ax=ax)  # Tạo một bản đồ

        m.readshapefile('st99_d00', 'states')  #Đọc file shapefile và vẽ các state lên bản đồ
        for state, coords in state_coords.items():
            lon, lat = coords
            x, y = m(lon, lat)
            plt.text(x, y, state, fontsize=7, fontweight = 'bold', ha='center', va='center', color='red', fontname = 'Georgia')
        for info, shape in zip(m.states_info, m.states):
            if info['NAME'] in states_to_fill:
                poly = Polygon(shape, facecolor='yellow')
                plt.gca().add_patch(poly)
        # Tạo chú thích và scatter cho các bang có tên là số
        for i, name in states_digit.items():
            lon, lat = state_coords[i]  # Lấy tọa độ tương ứng
            x, y = m(lon, lat)  # Chuyển đổi tọa độ
            plt.scatter(x, y, label=f'{i}: {name}')
        
        fig.legend(title = 'Map Annotation' , loc='upper center', ncol=2, prop={'family': 'Georgia'})
        canvas = FigureCanvasTkAgg(fig, master=self)  # Nhúng figure vào cửa sổ tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)  # Đặt canvas vào cửa sổ tkinter
    def cbo_chon_bang_click(self, *args):
        self.chon_bang = self.cbo_chon_bang.get()
    def cbo_ke_2_bang_click(self, *args):
        self.ke_2_bang = self.cbo_ke_2_bang.get()
    def btn_bang_ke_click(self):
        states_to_fill = []
        self.text_widget_1.delete('1.0', tk.END)
        output = run(0, self.x, self.adjacent(self.chon_bang, self.x))
        for item in output:
            self.text_widget_1.insert(tk.END, item + '\n', 'center')
            states_to_fill.append(item)
        self.text_widget_1.grid(row=0, column=0, padx=5, pady=5, sticky = tk.EW)
        self.ve_ban_do(states_to_fill)

    def btn_ke_ven_bien_click(self):
        states_to_fill = []
        self.text_widget_2.delete('1.0', tk.END)
        output = run(0, self.x, self.adjacent(self.chon_bang, self.x), self.coastal(self.x))
        for item in output:
            self.text_widget_2.insert(tk.END, item + '\n', 'center')
            states_to_fill.append(item)
        self.ve_ban_do(states_to_fill)
        if len(states_to_fill) == 0:
            messagebox.showinfo("Notification", "There are no states adjacent to " + self.chon_bang + " that are coastal")
            self.text_widget_2.delete('1.0', tk.END)
        self.text_widget_2.grid(row=0, column=0, padx=5, pady=5, sticky = tk.EW)
    def btn_ke_2_bang_click(self):
        states_to_fill = []
        self.text_widget_3.delete('1.0', tk.END)
        if self.cbo_ke_2_bang.get() == '':
            messagebox.showinfo("Notification", "Please select the second state")
            return 0
        output = run(0, self.x, self.adjacent(self.chon_bang, self.x), self.adjacent(self.ke_2_bang, self.x))
        for item in output:
            states_to_fill.append(item)
            self.text_widget_3.insert(tk.END, item + '\n', 'center')
        self.ve_ban_do(states_to_fill)
        if len(states_to_fill) == 0:
            messagebox.showinfo("Notification", "There are no states that are adjacent to " + self.chon_bang + " and " + self.ke_2_bang)
            self.text_widget_3.delete('1.0', tk.END)
        self.text_widget_3.grid(row=0, column=0, padx=5, pady=5, sticky = tk.EW)

if __name__ == '__main__':
    app = App()
    app.mainloop()