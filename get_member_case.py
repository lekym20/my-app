import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox

excel_file = os.path.join(
   os.path.dirname(os.path.abspath(__file__)),
   "DummyData.xlsx")

# Load Excel once when the program starts
df = pd.read_excel("DummyData.xlsx")
file_name = "DummyData.xlsx"
def get_member_case(member_id, program_type, policy_no):
   sheet_name = "Member Case"
   column_name = "MC_Member_ID"
   try:
    df = pd.read_excel(
        file_name,
        sheet_name
    )
    search_value = member_id
    matches = df[df["MC_Member_ID"] == search_value]
    member_record = matches.iloc[0]

    discharge_date = member_record["MC_Discharge_Date"]
    case_status = member_record["MC_Case_Status"]
    mc_member_id = member_record["MC_Member_ID"]

    # Display result
    if not matches.empty:
        if member_id == mc_member_id:
            if case_status == "Open" and discharge_date is not None:
                print("Inpatient Alert - Not eligible")
                messagebox.showwarning(
                "Inpatient Alert",
                "Member is NOT eligible. Please create a surveillance assignment.")
            else:
                # check program type in SAI
                if program_type in("PHS 2.0", "PHS 3.0"):
                    print("Check Policy number in MGRL")
                    check_policy_mgrl(policy_no)
                else:
                    messagebox.showerror(
                        "Check Program Type",
                        "Member is NOT eligible. Please reassign to real time work queue ."
                    )
        else:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Not found.")

   except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid numeric Member Program ID.")

def check_policy_mgrl(policy_no):
    sheet_name = "MGRL"
    print("Hello policy" +str(policy_no))
    try:
        print("Inside check_policy_mgrl with policy# " + str(policy_no))
        df = pd.read_excel(
            file_name,
            sheet_name
        )
        search_value = policy_no
        matches = df[df["Mgrl_Policy_No"] == search_value]
        if pd.isna(policy_no):
            print("Policy number is missing. Check the Policy end date")
            return None

        member_record = matches.iloc[0]

        policy_number = member_record["Mgrl_Policy_No"]

        # display result
        if not matches.empty:
            if policy_no == policy_number:
                print(f"Policy found in MGRL, policy no. {policy_no}")
        else:
            print("Check the End date or alerts for termed policy")

    except ValueError:
        messagebox.showerror(
            "Record not found",
            "Policy number not found."
        )

def get_prog_dtls(program_id):
    sheet_name = "ICUE - Program Dtls"
    try:
        df = pd.read_excel(
            file_name,
            sheet_name
        )
        search_value = program_id
        matches = df[df["Program_Id"] == search_value]
        member_record = matches.iloc[0]

        prog_id = member_record["Program_Id"]
        prog_code = member_record["Program_Code"]
        prog_name = member_record["Program_Name"]
        prog_type = member_record["Program_type"]

        # display result
        if not matches.empty:
            if program_id == prog_id:
                print("inside get_prog_dtls " + str(prog_id))
                return prog_code, prog_type
    except ValueError:
        messagebox.showerror(
            "Record not found",
            "Program ID not found."
        )