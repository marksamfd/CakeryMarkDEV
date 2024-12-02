import React from "react";

function Title({ children }) {
  const titleStyle = {
    marginBottom: '50px',
    color: 'black',
    fontSize: 50,
    fontFamily: 'Playfair Display',
    fontStyle: 'italic',
    fontWeight: 700,
    lineHeight: '60px',
    wordWrap: 'break-word',
  };

  return (
    <div style={titleStyle}>
      {children}
    </div>
  );
}

export default Title;
