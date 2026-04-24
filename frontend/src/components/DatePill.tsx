type Props = {
  date: Date;
  isSelected: boolean;
  onClick: () => void;
};

const dayAbbrevs = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export function DatePill({ date, isSelected, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-center justify-center w-[70px] h-[85px] rounded-[15px] shrink-0 transition-colors ${
        isSelected
          ? "bg-accent text-white"
          : "bg-card text-muted-foreground"
      }`}
    >
      <span className={`text-[30px] leading-none font-light ${isSelected ? "text-white" : "text-foreground"}`}>
        {date.getDate()}
      </span>
      <span className="text-[18px] mt-1">{dayAbbrevs[date.getDay()]}</span>
    </button>
  );
}
