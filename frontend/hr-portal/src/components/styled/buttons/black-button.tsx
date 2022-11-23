import styled from 'styled-components';

export const BlackButton = styled.button`
  background-color: #fff;
  color: black;
  border: 1px solid black;
  border-radius: 80px;

  padding: 16px 24px;
  margin-left: 25px;
  white-space: nowrap;
  
  &:hover {
    background-color: #000;
    color: #fff;
  }
  
  &:active {
    background-color: #000;
    color: #aaa;
  }
  
  &:disabled {
    color: #333;
  }
`;
