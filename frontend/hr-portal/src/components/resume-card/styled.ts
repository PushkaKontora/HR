import styled from 'styled-components';
import {XLargeRegular} from '../styled/fonts/x-large';
import {MediumRegular} from '../styled/fonts/medium';
import React from 'react';

export const Icon = styled.img`
  width: 22px;
  height: 22px;
  
  margin-right: 6px;
`;

export const UserIcon = styled.img`
  width: 129px;
  height: 129px;
  
  border-radius: 50%;
  object-fit: cover;
`;

export const ResumeField = styled.div`
  margin-top: 8px;
  vertical-align: middle;
`;

export const Contacts = styled(XLargeRegular)`
  display: flex;
  align-items: center;
  
  background-color: white;
  border-radius: 27px;
  padding: 18px 24px;
  color: black;
`;

export const CompetencyItem = styled(MediumRegular)`
  padding: 5px 15px;
  margin-right: 9px;
  color: #000;
  border-radius: 20px;
`;
