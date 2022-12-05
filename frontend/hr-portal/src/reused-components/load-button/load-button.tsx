import upload from '../../assets/icons/upload.svg';
import uploadWhite from '../../assets/icons/upload_white.svg';
import styled from 'styled-components';
import {useState} from 'react';

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
  width: 20px;
  height: 20px;
`;

type LoadButtonProps = {
  onClick: () => void;
  bgColor?: string
}

export function LoadButton({onClick, bgColor}: LoadButtonProps) {
  const [iconSrc, setIconSrc] = useState(upload);

  return (
    <Button
      bgColor={bgColor}
      onClick={onClick}
      type={'button'}
      onMouseEnter={() => setIconSrc(uploadWhite)}
      onMouseLeave={() => setIconSrc(upload)}>
      <Icon src={iconSrc}/>
    </Button>
  );
}