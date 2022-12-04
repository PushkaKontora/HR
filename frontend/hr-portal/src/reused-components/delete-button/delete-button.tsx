import styled from 'styled-components';
import {useState} from 'react';
import deleteIcon from '../../assets/icons/delete-cross.svg';
import whiteDeleteIcon from '../../assets/icons/delete-cross-white.svg';

export const Button = styled.button<{bgColor: string | undefined}>`
  background-color: ${props => props.bgColor || '#F6F5F3'};
  border-radius: 50%;
  
  width: 42px;
  height: 42px;
  
  margin-left: 8px;
  
  &:hover {
    background-color: #000;
  }
`;

export const Icon = styled.img`
  width: 16px;
  height: 16px;
`;

type LoadButtonProps = {
  onClick: () => void;
  bgColor?: string
}

export function DeleteButton({onClick, bgColor}: LoadButtonProps) {
  const [iconSrc, setIconSrc] = useState(deleteIcon);

  return (
    <Button
      bgColor={bgColor}
      onClick={onClick}
      type={'button'}
      onMouseEnter={() => setIconSrc(whiteDeleteIcon)}
      onMouseLeave={() => setIconSrc(deleteIcon)}>
      <Icon src={iconSrc}/>
    </Button>
  );
}