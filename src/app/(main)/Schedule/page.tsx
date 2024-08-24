import ShiftForm from "@/app/components/ShiftForm";
import ShiftApply from "@/app/components/ShiftApply";
import Calendar from "@/app/components/Calendar";

const SubmitPage = () => {
  return (
    <div className="font-semibold bg-gray-50 m-1 items-center ">
      <div>
        <ShiftApply />
      </div>
    </div>
  );
};

export default SubmitPage;
