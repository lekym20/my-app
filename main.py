import os
import sys
import get_member_case as mbrcse
from test_app.get_member_case import get_member_case

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Package locations:", sys.path)

import pandas as pd
import tkinter as tk
from tkinter import messagebox

excel_file = os.path.join(
   os.path.dirname(os.path.abspath(__file__)),
   "DummyData.xlsx")

# Load Excel once when the program starts
df = pd.read_excel("DummyData.xlsx")

v_program_id = ""
file_name = "DummyData.xlsx"
def search_member():
    try:
        # Get value from textbox
        search_value = int(entry.get())

        # Search in dataframe
        matches = df[df["Member_Prog_Id"] == search_value]
        member_record = matches.iloc[0]

        member_prog_id = member_record["Member_Prog_Id"]
        member_name = member_record["Member_First_Name"]
        opt_out_preference = member_record["Member_Opt_Out_Preference"]
        member_age = member_record["Member_Age"]
        member_id = member_record["Member_ID"]
        member_policy_no = member_record["Member_Policy_No"]
        program_code, program_type = mbrcse.get_prog_dtls(member_prog_id)

        # Display result
        if not matches.empty:
            # result_text.delete("1.0", tk.END)
            # result_text.insert(tk.END, matches.to_string(index=False))
            # 1. Check Opt out preference
            if opt_out_preference == "DNC":
                print("Not eligible")
                messagebox.showwarning(
                    "Opt Out Preference",
                    "Member is NOT eligible. Opt Out Preference is set to DNC. Please process reject referral."
                )
            # 2. Validate Age eligibility
            elif member_age > 18:

                print("Eligible age")
                # Check for inpatient alert
                print(member_id)
                mbrcse.get_member_case(member_id, program_type, member_policy_no)

            else:
                # Check Case if GCM
                # program_code, program_type = get_prog_dtls(member_prog_id)
                print(program_code)
                print(program_type)
                if program_code == "GCM":
                    print("Check for inpatient alert")
                    print(member_id)
                    mbrcse.get_member_case(member_id, program_type, member_policy_no)
                else:
                    messagebox.showwarning(
                        "Case Type check",
                        "Member age is below 18 yrs old and is NOT eligible. Please create a GCM referral"
                    )

        else:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Not found.")

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid numeric Member Program ID.")

# Create window
root = tk.Tk()
root.title("Member Search")
root.geometry("1200x600")

# Label
label = tk.Label(root, text="Member Program ID:")
label.pack(pady=5)

# Input field
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=search_member)
search_button.pack(pady=10)

# Results area
result_text = tk.Text(root, height=20, width=140)
result_text.pack(pady=10)

root.mainloop()
