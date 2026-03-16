interface Props {
  options: readonly string[];
  selected: string;
  onChange: (val: string) => void;
  label?: string;
}

export function FilterChips({ options, selected, onChange, label }: Props) {
  return (
    <div className="flex items-center gap-2 overflow-x-auto horizontal-scroll pb-1" data-testid="filter-chips">
      {label && (
        <span className="text-xs font-medium text-muted-foreground flex-shrink-0 mr-1">{label}</span>
      )}
      {options.map((opt) => (
        <button
          key={opt}
          onClick={() => onChange(opt)}
          className={`flex-shrink-0 text-xs font-medium px-3 py-1.5 rounded-full border transition-all duration-150 capitalize ${
            selected === opt
              ? "bg-primary text-primary-foreground border-primary"
              : "bg-transparent text-muted-foreground border-border/50 hover:text-foreground hover:border-border"
          }`}
          data-testid={`chip-${opt.toLowerCase().replace(/\s+/g, '-')}`}
        >
          {opt}
        </button>
      ))}
    </div>
  );
}

interface ToggleProps {
  label: string;
  active: boolean;
  onChange: (val: boolean) => void;
}

export function FilterToggle({ label, active, onChange }: ToggleProps) {
  return (
    <button
      onClick={() => onChange(!active)}
      className={`flex-shrink-0 text-xs font-medium px-3 py-1.5 rounded-full border transition-all duration-150 ${
        active
          ? "bg-primary/20 text-primary border-primary/50"
          : "bg-transparent text-muted-foreground border-border/50 hover:text-foreground hover:border-border"
      }`}
      data-testid={`toggle-${label.toLowerCase().replace(/\s+/g, '-')}`}
    >
      {active ? "★ " : ""}{label}
    </button>
  );
}
