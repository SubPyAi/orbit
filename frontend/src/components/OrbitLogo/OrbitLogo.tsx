const OrbitLogo = ({ 
  size = 20, 
  color = '#3D8A5A', 
  className = '', 
  style = {},
  ...props 
}) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ display: 'block', flexShrink: 0, ...style }}
      {...props}
    >
      <g id="planet">
        {/* Outer Circle */}
        <circle
          id="Oval 2"
          cx="10.00002"
          cy="9.99998951"
          r="8.33333302"
          stroke={color}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="1.666667"
        />

        {/* Inner Crescent Arc */}
        <path
          id="Vector 22"
          d="M10 1.66666C9.12009 2.54657 8.54133 3.68246 8.34666 4.91152C8.152 6.14059 8.35143 7.39973 8.91637 8.50849C9.4813 9.61724 10.3828 10.5187 11.4915 11.0836C12.6003 11.6486 13.8594 11.848 15.0885 11.6533C16.3175 11.4587 17.4534 10.8799 18.3333 9.99999"
          fillRule="nonzero"
          stroke={color}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="1.666667"
        />
      </g>
    </svg>
  );
};

export default OrbitLogo;