import type React from "react";
import "./Button.css";

function Button(
  {
    text,
    onClickFunction,
    bkg,
    col,
    hoverCol,
    hoverGlowCol,
    height,
    width,
    borderRadius,
    border = "none"
  }: {
    text: string,
    onClickFunction: () => void,
    bkg: string,
    col: string,
    hoverCol: string,
    hoverGlowCol: string,
    height: string,
    width: string,
    borderRadius: string,
    border?: string
  }
) {
  return (
    <div className="button-wrapper" style={{"--height": height} as React.CSSProperties}>
      <button
        className="button-wrapper-button"
        onClick={onClickFunction}
        style={
          {
            "--bg-col": bkg,
            "--col": col,
            "--hover-bg": hoverCol,
            "--height": height,
            "--width": width,
            "--border-radius": borderRadius,
            "--border": border
          } as React.CSSProperties
        }
      >
        {text}
      </button>
    </div>
  );
}

export default Button;
