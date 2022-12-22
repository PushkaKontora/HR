import {OptionType, ProfileSelect} from '../profile-select/profile-select';
import {useAppDispatch, useAppSelector} from '../../../app/hooks';
import {useEffect, useState} from 'react';
import {getCompetenciesAction} from '../../../service/async-actions/async-actions-competencies';

export type CompetenciesSelectProps = {
  name: string,
  onChange: (e: any) => void,
  selectedComps: string[],
  width?: string
}

export function CompetenciesSelect({name, onChange, selectedComps, width}: CompetenciesSelectProps) {
  const dispatch = useAppDispatch();

  const comps = useAppSelector((state) => state.general.competencies);
  const options = comps.map((item) => {
    return {
      'value': item.name,
      'label': item.name
    };
  });

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      dispatch(getCompetenciesAction());
    }

    return () => {
      mounted = false;
    };
  }, []);


  return (
    <ProfileSelect
      name={name}
      onChange={onChange}
      options={options}
      placeholder={'Выбрать компетенцию'}
      selectedOptions={selectedComps}
      width={width}/>
  );
}
