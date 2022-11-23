import {ResumeTitle} from '../components/styled/resume/resume-title';
import {CompetencyFlexContainer} from '../components/styled/values/competency-flex-container';
import {useAppSelector} from '../app/hooks';
import {useEffect, useState} from 'react';

export type CompetencyListProps = {
  values: string[]
}

export function CompetencyList({values}: CompetencyListProps) {
  const [valuesState, setValuesState] = useState(values);

  useEffect(() => {
    setValuesState(values);
  }, [values]);

  return (
    <CompetencyFlexContainer>
      {
        valuesState.map((item, idx) => {
          return (<ResumeTitle style={{marginRight: '8px'}} key={idx}>{item}</ResumeTitle>);
        })
      }
    </CompetencyFlexContainer>
  );
}