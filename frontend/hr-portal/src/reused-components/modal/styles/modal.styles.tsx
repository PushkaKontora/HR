import styled from 'styled-components';

interface ModalContentProps {
  width?: number,
  padding?: string
}

export const ModalContent = styled.div.attrs<ModalContentProps>((props) => ({
  width: (props.width || 886) + 'px',
}))<ModalContentProps>`
  background: #FFFFFF;
  border-radius: 37.1429px;
  padding: ${({padding = '80px 80px 60px 80px'}) => padding};
  width: ${({width}) => width};
  position: relative;

  min-height: 100px;
  max-height: 80vh;

  overflow: auto;
`;

