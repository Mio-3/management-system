"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import useSWR from "swr";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import NightlightIcon from "@mui/icons-material/Nightlight";
import MoreTimeIcon from "@mui/icons-material/MoreTime";
import CloseIcon from "@mui/icons-material/Close"; 

interface Holiday {
  date: string;
  title: string;
}

interface Shift {
  date: string;
  category: string;
}

const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error("Failed to fetch holiday data");
  }
  const data = await res.json();
  return data.map((holiday: { date: string; localName: string }) => ({
    date: holiday.date,
    title: holiday.localName,
  }));
};

const Calendar = () => {
  const { data: events, error } = useSWR<Array<Holiday>>("https://date.nager.at/api/v3/NextPublicHolidays/JP", fetcher);

  if (error) return <div>Failed to load</div>;
  if (!events) return <div>Loading...</div>;

  return (
    <div>
      <FullCalendar
        locale={"ja"}
        plugins={[dayGridPlugin]}
        initialView="dayGridMonth"
        height="auto"
        timeZone="Asia/Tokyo"
        events={events.map((event) => ({
          title: event.title,
          date: event.date,
          backgroundColor: "transparent",
          textColor: "red",
          borderColor: "transparent",
          classNames: "holiday-event",
        }))}
        headerToolbar={{
          start: "prev",
          center: "title",
          end: "next",
        }}
        buttonText={{
          month: "月",
        }}
        buttonHints={{
          prev: "先$0",
          next: "来$0",
        }}
        views={{
          dayGridMonth: {
            titleFormat: { month: "long" },
          },
        }}
        dayCellContent={(arg) => `${arg.date.getDate()}`}
      />
    </div>
  );
};

export default Calendar;
