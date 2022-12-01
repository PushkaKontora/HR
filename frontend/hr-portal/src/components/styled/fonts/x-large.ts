import styled from 'styled-components';

interface BtnWrapperProps {
  width?: string,
}

export const XLargeRegular = styled.div.attrs<BtnWrapperProps>((props) => ({
  width: (props.width || '100%'),
}))<BtnWrapperProps>`
  font-weight: 400;
  font-size: 18px;
  line-height: 18px;
  letter-spacing: 0.05em;

  width: ${({width}) => width};
`;

export const XLargeLight = styled(XLargeRegular)`
  font-weight: 300;
`;

export const XLargeMedium = styled(XLargeRegular)`
  font-weight: 500;
`;
