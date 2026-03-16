export function Logo({ size = 24 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="PHL Underground logo"
    >
      {/* Outer circle — compass ring */}
      <circle cx="24" cy="24" r="22" stroke="currentColor" strokeWidth="2" />
      {/* Grid lines — city grid */}
      <line x1="24" y1="6" x2="24" y2="42" stroke="currentColor" strokeWidth="1.5" opacity="0.4" />
      <line x1="6" y1="24" x2="42" y2="24" stroke="currentColor" strokeWidth="1.5" opacity="0.4" />
      {/* U shape — Underground */}
      <path
        d="M15 14V30C15 35 19 38 24 38C29 38 33 35 33 30V14"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Compass diamond at top */}
      <path d="M24 2L26.5 6L24 5L21.5 6Z" fill="currentColor" />
    </svg>
  );
}
