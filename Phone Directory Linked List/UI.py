from tkinter import *
from tkinter import ttk
import pickle
from functools import partial
from linked_list import LinkedList

BACKGROUND_COLOR = "#F5F5F5"
CONTACT_BUTTON_COLOR ="#E8E8E8"
ADD_CONTACT_BUTTON_COLOR = "#72A0C1"
DELETE_BUTTON_COLOR = "#005A9C"
EDIT_BUTTON_COLOR = "#B9D9EB"
Gray_COLOR = "gray"
SEARCH_COLOR_BUTTON = "#585858"

class PhoneDirectoryInterface():
    def __init__(self, *args, **kwargs):
        self.window = Tk()
        # self.window.minsize(width=300, height=500)

        self.window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
        self.linkedList = LinkedList()
        self.addedToPage = []
        self.contact_detail_list = []
        self.contact_list_page(True)

        self.window.mainloop()

    def addScroll(self):
        # Create A Main frame
        main_frame = Frame(self.window)
        main_frame.pack(fill=BOTH, expand=1)
        self.addedToPage.append(main_frame)

        # Create A Canvas
        my_canvas = Canvas(main_frame, bg=BACKGROUND_COLOR)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.addedToPage.append(my_canvas)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        self.addedToPage.append(my_scrollbar)

        # Configure The Canvas
        my_canvas.configure(yscrollcomman=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        return second_frame

    def destroy_widgets(self):
        for item in self.addedToPage:
            item.destroy()
        self.addedToPage = []

    # ---------------------------- Contact List Page ------------------------------- #

    def contact_list_page(self, flag):
        self.destroy_widgets()

        application_title = Label(text="Contacts", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        application_title.pack(side=TOP)
        self.addedToPage.append(application_title)

        search_input_frame = Frame(self.window)
        search_input_frame.pack(anchor="w")
        search_label = Label(search_input_frame, text="Search Name: ", font=("Arial", 12, "bold"), bg=BACKGROUND_COLOR)
        search_label.pack(side=LEFT)
        search_input = Entry(search_input_frame, width=40)
        search_input.pack(side=LEFT)
        search_button = Button(search_input_frame, text="Search", font=("Arial", 12, "bold"), command=lambda: self.search_page(search_input.get()), relief=FLAT, fg="white", bg=SEARCH_COLOR_BUTTON)
        search_button.pack(side=LEFT)
        self.addedToPage.extend([search_input_frame, search_input, search_button])

        second_frame = self.addScroll()

        with open("contact_data.txt", mode="rb") as file:
            contact_list = pickle.load(file)

        if flag:
            for contact in contact_list:
                self.linkedList.insert(name=contact["name"], address=contact["address"], contact_number=contact["contact_number"], email=contact["email"])

        i = 0
        temp = self.linkedList.return_head()
        self.contact_detail_list = []
        while temp is not None:
            name_Button = Button(second_frame, text=temp.name, font=("Arial", 12, "bold"), command=partial(self.contact_detail_page, i), width=40, relief=FLAT, anchor="w", bg=CONTACT_BUTTON_COLOR)
            name_Button.pack()
            line_separator = ttk.Separator(second_frame, orient='horizontal')
            line_separator.pack(fill='x')
            self.addedToPage.extend([name_Button,line_separator])

            self.contact_detail_list.append({"name": temp.name, "address": temp.address, "contact_number": temp.contact_number, "email": temp.email})
            temp = temp.next
            i += 1

        addContact = Button(text="Add Contact", font=("Arial", 12, "bold"), width=12, command=self.add_contact_page, relief=FLAT, fg="white", bg=ADD_CONTACT_BUTTON_COLOR)
        addContact.pack(padx=10, pady=(0, 10), side=BOTTOM)
        save_Button = Button(text='Save Changes', font=("Arial", 12, "bold"), width=12, command=self.save_changes, relief=FLAT, anchor="w", fg="white", bg=EDIT_BUTTON_COLOR)
        save_Button.pack(side=BOTTOM, pady=(10, 0))
        self.addedToPage.extend([addContact, save_Button])

    def save_changes(self):
        temp = self.linkedList.return_head()
        save_contact_list = []

        while temp is not None:
            object = {"name": temp.name, "address": temp.address, "contact_number": temp.contact_number, "email": temp.email}
            save_contact_list.append(object)
            temp = temp.next
        with open("contact_data.txt", mode="wb") as file:
            pickle.dump(save_contact_list, file)

    # -------------------------- Display Contact Detail----------------------------- #

    def contact_detail_page(self, index, search_name=None):
        def return_to_main_or_searchPage():
            if search_name is None:
                self.contact_list_page(False)
            else:
                self.search_page(search_name)

        self.destroy_widgets()

        title = Label(text="Contact Details", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        name, address, contact_number, email = self.contact_detail_list[index]["name"], self.contact_detail_list[index]["address"], self.contact_detail_list[index]["contact_number"], self.contact_detail_list[index]["email"]

        name_frame = Frame(self.window)
        name_frame.pack(anchor="w")
        name_label = Label(name_frame, text="Name ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        name_label.pack(anchor='w', side=LEFT)
        name_output = Label(name_frame, text=name, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        name_output.pack(anchor='w', side=LEFT)
        line_separator = ttk.Separator(self.window, orient='horizontal')
        line_separator.pack(fill='x')
        self.addedToPage.extend([name_frame, name_label, name_output, line_separator])

        email_number_frame = Frame(self.window)
        email_number_frame.pack(anchor="w")
        email_label = Label(email_number_frame, text="Email ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        email_label.pack(anchor='w', side=LEFT)
        email_output = Label(email_number_frame, text=email, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        email_output.pack(anchor='w', side=LEFT)
        line_separator = ttk.Separator(self.window, orient='horizontal')
        line_separator.pack(fill='x')
        self.addedToPage.extend([email_number_frame, email_label, email_output, line_separator])

        address_frame = Frame(self.window)
        address_frame.pack(anchor="w")
        address_label = Label(address_frame, text="Address ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        address_label.pack(anchor='w', side=LEFT)
        address_output = Label(address_frame, text=address, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        address_output.pack(anchor='w', side=LEFT)
        line_separator2 = ttk.Separator(self.window, orient='horizontal')
        line_separator2.pack(fill='x')
        self.addedToPage.extend([address_frame, address_label, address_output, line_separator2])

        contact_number_frame = Frame(self.window)
        contact_number_frame.pack(anchor="w")
        contact_number_label = Label(contact_number_frame, text="Contact Number ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        contact_number_label.pack(anchor='w', side=LEFT)
        contact_number_output = Label(contact_number_frame, text=contact_number, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        contact_number_output.pack(anchor='w', side=LEFT)
        self.addedToPage.extend([contact_number_frame, contact_number_label, contact_number_output])


        back_button = Button(text="Back", font=("Arial", 12, "bold"), command=return_to_main_or_searchPage, relief=FLAT, width=6, fg="white", bg=ADD_CONTACT_BUTTON_COLOR)
        back_button.pack(side=BOTTOM)
        delete_button = Button(text="Delete", font=("Arial", 12, "bold"), command=lambda: self.delete_contact(name, address, contact_number, email), width=6, fg="white", relief=FLAT, bg=DELETE_BUTTON_COLOR)
        delete_button.pack(side=BOTTOM)
        edit_button = Button(text="Edit", font=("Arial", 12, "bold"), command=lambda: self.edit_contact_page(name, address, contact_number, email), width=6, fg="white", relief=FLAT, bg=EDIT_BUTTON_COLOR)
        edit_button.pack(side=BOTTOM, pady=(100, 0))
        self.addedToPage.extend([edit_button, delete_button, back_button])


    def delete_contact(self, name, address, contact_number, email):
        self.linkedList.delete_node(name, address, contact_number, email)
        self.contact_list_page(False)

    # ----------------------------- Edit Contact Page ------------------------------ #

    def edit_contact_page(self, name, address, contact_number, email):
        self.destroy_widgets()
        entry_length = 80
        previous_record = [name, address, contact_number, email]

        title = Label(text="Edit Contact", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        name_frame = Frame(self.window)
        name_frame.pack(anchor="w")
        name_label = Label(name_frame, text="Name ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        name_label.pack(anchor='w', side=LEFT)
        name_input = Entry(name_frame, width=(entry_length + 3))
        name_input.insert(END,name)
        name_input.pack(side=LEFT)
        self.addedToPage.extend([name_frame, name_label, name_input])

        email_frame = Frame(self.window)
        email_frame.pack(anchor="w")
        email_label = Label(email_frame, text="Email ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        email_label.pack(anchor='w', side=LEFT)
        email_input = Entry(email_frame, width=(entry_length + 4))
        email_input.insert(END, email)
        email_input.pack(side=LEFT)
        self.addedToPage.extend([email_frame, email_label, email_input])

        address_frame = Frame(self.window)
        address_frame.pack(anchor="w")
        address_label = Label(address_frame, text="Address ", font=("Arial", 12, "bold"), anchor="e",
                              bg=BACKGROUND_COLOR)
        address_label.pack(anchor='w', side=LEFT)
        address_input = Entry(address_frame, width=entry_length)
        address_input.insert(END, address)
        address_input.pack(side=LEFT)
        self.addedToPage.extend([address_frame, address_label, address_input])

        contact_number_frame = Frame(self.window)
        contact_number_frame.pack(anchor="w")
        contact_number_label = Label(contact_number_frame, text="Contact Number ", font=("Arial", 12, "bold"),
                                     anchor="e", bg=BACKGROUND_COLOR)
        contact_number_label.pack(anchor='w', side=LEFT)
        contact_number_input = Entry(contact_number_frame, width=(entry_length - 10))
        contact_number_input.insert(END, contact_number)
        contact_number_input.pack(side=LEFT)
        self.addedToPage.extend([contact_number_frame, contact_number_label, contact_number_input])

        update_button = Button(text="Update", font=("Arial", 12, "bold"), fg="white", command=lambda: self.update_contact(previous_record[0], previous_record[1], previous_record[2], previous_record[3], name_input.get(), address_input.get(), contact_number_input.get(), email_input.get()), relief=FLAT, bg=DELETE_BUTTON_COLOR)
        update_button.pack()
        cancel_button = Button(text="Cancel", font=("Arial", 12, "bold"), command=lambda: self.contact_list_page(False), relief=FLAT, width=6, fg="white", bg=Gray_COLOR)
        cancel_button.pack()
        self.addedToPage.extend([update_button, cancel_button])

    def update_contact(self, prev_name, prev_address, prev_contact_number, prev_email, name, address, contact_number, email):
        self.linkedList.update(prev_name, prev_address, prev_contact_number, prev_email, name, address, contact_number, email)
        self.contact_list_page(False)

    # ----------------------------- Add Contact Page ------------------------------- #

    def add_contact_page(self):
        self.destroy_widgets()
        entry_length = 80

        title = Label(text="Add Contact", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        name_frame = Frame(self.window)
        name_frame.pack(anchor="w")
        name_label = Label(name_frame, text="Name ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        name_label.pack(anchor='w', side=LEFT)
        name_input = Entry(name_frame, width=(entry_length + 3))
        name_input.pack(side=LEFT)
        self.addedToPage.extend([name_frame, name_label, name_input])

        email_frame = Frame(self.window)
        email_frame.pack(anchor="w")
        email_label = Label(email_frame, text="Email ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        email_label.pack(anchor='w', side=LEFT)
        email_input = Entry(email_frame, width=(entry_length + 4))
        email_input.pack(side=LEFT)
        self.addedToPage.extend([email_frame, email_label, email_input])

        address_frame = Frame(self.window)
        address_frame.pack(anchor="w")
        address_label = Label(address_frame, text="Address ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        address_label.pack(anchor='w', side=LEFT)
        address_input = Entry(address_frame, width=entry_length)
        address_input.pack(side=LEFT)
        self.addedToPage.extend([address_frame, address_label, address_input])

        contact_number_frame = Frame(self.window)
        contact_number_frame.pack(anchor="w")
        contact_number_label = Label(contact_number_frame, text="Contact Number ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        contact_number_label.pack(anchor='w', side=LEFT)
        contact_number_input = Entry(contact_number_frame, width=(entry_length - 10))
        contact_number_input.pack(side=LEFT)
        self.addedToPage.extend([contact_number_frame, contact_number_label, contact_number_input])

        notice_frame = Frame(self.window)
        notice_frame.pack(anchor="w")
        notice_label = Label(notice_frame, text="Enter at least name and contact number for the new contact to be added.", font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        notice_label.pack(anchor='w', side=LEFT)
        self.addedToPage.extend([notice_label, notice_frame])

        add_button = Button(text="Add", font=("Arial", 12, "bold"), command=lambda: self.add_contact(name_input.get(),address_input.get(),contact_number_input.get(),email_input.get()), width=6, fg="white", relief=FLAT, bg=ADD_CONTACT_BUTTON_COLOR)
        back_button = Button(text="Back", font=("Arial", 12, "bold"), width=6, command=lambda: self.contact_list_page(False), fg="white", relief=FLAT, bg=Gray_COLOR)
        back_button.pack(side=BOTTOM)
        add_button.pack(side=BOTTOM)
        self.addedToPage.extend([add_button,back_button])

    def add_contact(self, name, address, contact_number, email):
        if len(name) > 0 and len(contact_number) > 0:
            self.linkedList.insert(name=name, address=address, contact_number=contact_number, email=email)
        self.contact_list_page(False)

    # -------------------------------- Search Page --------------------------------- #

    def search_page(self, name):
        self.destroy_widgets()

        title = Label(text="Search Found", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        prefix_match_found = []
        name = name.lower()
        len_name = len(name)

        for item in self.contact_detail_list:
            if len_name <= len(item["name"]):
                if name == item["name"][:len_name].lower():
                    prefix_match_found.append(item)

        i = 0
        second_frame = self.addScroll()
        for item in prefix_match_found:
            name_Button = Button(second_frame, text=item["name"], font=("Arial", 12, "bold"), command=partial(self.contact_detail_page, i, name), width=40, relief=FLAT, anchor="w", bg=CONTACT_BUTTON_COLOR)
            name_Button.pack()
            line_separator = ttk.Separator(second_frame, orient='horizontal')
            line_separator.pack(fill='x')
            self.addedToPage.extend([name_Button,line_separator])
            i += 1

        back_button = Button(text="Back", font=("Arial", 12, "bold"), width=6, command=lambda: self.contact_list_page(False), fg="white", relief=FLAT, bg=Gray_COLOR)
        back_button.pack(side=BOTTOM)
        self.addedToPage.append(back_button)
