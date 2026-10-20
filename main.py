import os
import sys
import get_member_case as mbrcse
from get_member_case import get_member_case
from datetime import date

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
v_not_eligible = "Based from the following parameters, Member is NOT eligible:\n"
v_action = "RECOMMENDED ACTION : "
v_reject_ref = "Process reject referral."
v_gcm_ref = "Create a GCM referral."
v_create_surv = "Create a surveillance assignment."
v_reassign = "Reassign to real time work queue."
member_policy_no = ""

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
        member_policy_end_date = member_record["Member_Policy_End_Date"]
        member_opt_out_date = member_record["Member_Opt_Out_Date"]
        program_code, program_type, program_name = mbrcse.get_prog_dtls(member_prog_id)

        # Display result
        if not matches.empty:
            # result_text.delete("1.0", tk.END)
            # result_text.insert(tk.END, matches.to_string(index=False))
            # 1. Check Opt out preference
            if opt_out_preference == "DNC":
                # SCENARIO 1
                print("Not eligible")
                messagebox.showwarning(
                    "SCENARIO 1: Opt Out Preference",
                    v_not_eligible +
                    "Opt Out Preference: DNC.\n"
                    "Member opt out date: " + member_opt_out_date.strftime("%m/%d/%Y") + "\n" +
                    v_action + v_reject_ref
                )
            # 2. Validate Age eligibility
            elif member_age > 18:

                print("Eligible age")
                # Check for inpatient alert
                print(member_id)
                mbrcse.get_member_case(member_id, program_type, member_policy_no,member_policy_end_date)

            else:
                # Check Case if GCM
                # program_code, program_type = get_prog_dtls(member_prog_id)
                print(program_code)
                print(program_type)
                if program_code == "GCM":
                    print("Check for inpatient alert")
                    print(member_id)
                    case_status, discharge_date = mbrcse.get_member_case(member_id, program_type, member_policy_no,member_policy_end_date)

                    # SCENARIO 3
                    if case_status == "Open" and pd.isna(discharge_date):
                        discharge_date = "Not yet discharged"
                        messagebox.showwarning(
                            "SCENARIO 3: Inpatient Alert",
                            v_not_eligible +
                            f"Age(in yrs) : {member_age}\n"
                            f"Program : {program_name}\n"
                            f"Case status : {case_status}\n"
                            f"Discharge date : {discharge_date}\n" +
                            v_action + v_create_surv)
                    else:
                        # SCENARIO 5
                        if program_type in("PHS 2.0", "PHS 3.0"):
                            print("Check Policy end date in MGRL")
                            print(mbrcse.check_policy_mgrl(member_policy_no, member_policy_end_date))
                            if mbrcse.check_policy_mgrl(member_policy_no, member_policy_end_date):
                                print("SCENARIO 5: Policy found in MGRL. Check the value of Member Facing Services")
                            else:
                                #member_policy_end_date = pd.to_datetime(member_policy_end_date, errors="coerce")
                                if pd.isna(member_policy_end_date):
                                    print("Policy end date is missing")
                                    print(member_policy_end_date)
                                elif member_policy_end_date.date() > date.today():
                                    print("SCENARIO 7: Validate Funding Arrangement")
                                else:
                                    messagebox.showerror(
                                        "SCENARIO 6: Check Policy End Date",
                                        v_not_eligible +
                                        f"Age(in yrs) : {member_age}\n"
                                        f"Program : {program_name}\n"
                                        f"Case status : {case_status}\n"
                                        f"Discharge date : {discharge_date}\n" +
                                        f"Program Type : {program_type}\n" +
                                        f"Policy End Date: {member_policy_end_date}\n" +
                                        "Policy record NOT found in MGRL.\n" +
                                        v_action + v_reject_ref
                                    )

                        # SCENARIO 4
                        else:
                            messagebox.showerror(
                                "SCENARIO 4: Check Program Type",
                                v_not_eligible +
                                f"Age(in yrs) : {member_age}\n"
                                f"Program : {program_name}\n"
                                f"Case status : {case_status}\n"
                                f"Discharge date : {discharge_date}\n" +
                                f"Program Type : {program_type}\n"+
                                v_action + v_reassign)

                # SCENARIO 2
                else:
                    messagebox.showwarning(
                        "SCENARIO 2: Case Type check",
                        v_not_eligible +
                        f"Member age is {member_age}\n"
                        f"Member Program: {program_name}\n" +
                        v_action + v_gcm_ref
                    )

        else:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Not found.")

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid numeric Member Program ID....")

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
