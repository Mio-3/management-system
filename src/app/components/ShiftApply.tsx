"use client";

import React, { useState } from "react";
import ShiftForm from "./ShiftForm";

const ShiftApply = () => {
  const [isEntryDrawerOpen, setIsEntryDrawerOpen] = useState(false);
  const [shifts, setShifts] = useState([]);

  const closeForm = () => {
    setIsEntryDrawerOpen(!isEntryDrawerOpen);
  };

  const handleAddShiftForm = () => {
    setIsEntryDrawerOpen(!isEntryDrawerOpen);
  };

  const handleSaveShift = (shift) => {
    setShifts([...shifts, shift]);
  };

  const handleSubmitShifts = () => {
    console.log(shifts);
  };

  return (
    <div className="flex flex-col items-center space-y-4 sm:space-y-0 sm:flex-row sm:justify-center sm:space-x-4">
      <div className="flex flex-col md:gap-8 sm:flex-row sm:gap-4">
        <button className="bg-blue-gray-500 hover:bg-blue-gray-700 text-white py-3 px-12 rounded-md mt-8 mb-6 transition hover:-translate-y-2 w-full sm:w-auto" onClick={handleAddShiftForm}>
          シフト申請
        </button>
        <button 
          className="bg-blue-gray-500 hover:bg-blue-gray-700 text-white py-3 px-12 rounded-md mt-8 mb-6 transition hover:-translate-y-2 w-full sm:w-auto"
          onClick={handleSubmitShifts}
        >
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
