"use client";

import React, { useState } from "react";
import ShiftForm, { ShiftFormValues } from "./ShiftForm";
import Calendar from "./Calendar";

interface ShiftEvent {
  title: string;
  date: string;
}

const ShiftApply = () => {
  const [isEntryDrawerOpen, setIsEntryDrawerOpen] = useState(false);
  const [shifts, setShifts] = useState<ShiftFormValues[]>([]);

  const closeForm = () => {
    setIsEntryDrawerOpen(!isEntryDrawerOpen);
  };

  const handleAddShiftForm = () => {
    setIsEntryDrawerOpen(!isEntryDrawerOpen);
  };

  const handleSaveShift = (shift: ShiftFormValues) => {
    setShifts((prevShifts) => {
      const existingShiftIndex = prevShifts.findIndex((s) => s.date === shift.date);

      if (existingShiftIndex !== -1) {
        const updatedShifts = [...prevShifts];
        updatedShifts[existingShiftIndex] = shift;
        return updatedShifts;
      } else {
        return [...prevShifts, shift];
      }
    });
  };

  const fetchShifts = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/shifts", {
        next: { revalidate: 10 }, // ISR
      });
      const data = await res.json();
      return data;
    } catch (error) {}
  };

  const handleSubmitShifts = async () => {
    shifts.forEach((shift) => {
      console.log(`Date: ${shift.date}, Category: ${shift.category}`);
    });
    try {
      const res = await fetch("http://127.0.0.1:8000/shifts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(shifts),
      });

      if (res.ok) {
        console.log("シフト申請が成功しました");
      } else {
        console.error("シフト申請に失敗しました");
      }
    } catch (error) {
      console.error("シフト申請に失敗しました");
    }
  };

  const updateShift = async (shiftId, updatedShift) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/shifts/${shiftId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedShift),
      });

      if (response.ok) {
        console.log("シフトが更新されました");
      } else {
        console.error("シフトの更新に失敗しました");
      }
    } catch (error) {
      console.error("ネットワークエラー:", error);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      <div className="w-full">
        <Calendar shifts={shifts} />
      </div>
      <div className="flex flex-col items-center gap-4 mt-8 w-full sm:flex-row sm:justify-center">
        <button className="bg-blue-gray-500 hover:bg-blue-gray-700 text-white py-3 px-12 rounded-md transition hover:-translate-y-2 w-full sm:w-auto" onClick={handleAddShiftForm}>
          シフト申請
        </button>
        <button className="bg-blue-gray-500 hover:bg-blue-gray-700 text-white py-3 px-12 rounded-md transition hover:-translate-y-2 w-full sm:w-auto" onClick={handleSubmitShifts}>
          シフト希望提出
        </button>
      </div>
      <div className="justify-end w-full sm:w-auto">
        <ShiftForm onSaveShift={handleSaveShift} onCloseForm={closeForm} isEntryDrawerOpen={isEntryDrawerOpen} />
      </div>
    </div>
  );
};

export default ShiftApply;
