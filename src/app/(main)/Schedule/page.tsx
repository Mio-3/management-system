import ShiftForm from "@/app/components/ShiftForm";
import Calendar from "../../components/Calendar";
import ShiftApply from "@/app/components/ShiftApply";

const SubmitPage = () => {
  
  return (
    <div className="font-semibold bg-gray-50 m-1 items-center ">
      <Calendar />
      <div>
        <ShiftApply />
      </div>
    </div>
  );
};

export default SubmitPage;