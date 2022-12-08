import Select, {OnChangeValue} from 'react-select';
import {useAppDispatch} from '../../app/hooks';
import {setCompetencies} from '../../features/vacancy/vacancy-slice';
import './competencies-field.scss';
import {useEffect, useState} from 'react';

export interface CompetenciesOption {
  readonly value: string;
  readonly label: string;
}

export const competenciesOptions: readonly CompetenciesOption[] = [
  {value: 'css', label: 'css'},
  {value: 'html', label: 'html'},
  {value: 'C#', label: 'C#'},
  {value: 'управление персоналом', label: 'управление персоналом'},
  {value: 'Python', label: 'Python'},
  {value: 'SQL', label: 'SQL'},
  {value: 'Angular', label: 'Angular'},
  {value: 'React', label: 'React'},
  {value: 'тестирование', label: 'тестирование'},
];

function CompetenciesField() {
  const [options, setOptions] = useState(competenciesOptions);
  const dispatch = useAppDispatch();

  const handlerOnChangeValue = (newValues: OnChangeValue<CompetenciesOption, boolean>) => {
    const newCompetence = (newValues as CompetenciesOption[]).map((item: CompetenciesOption) => item.value);
    dispatch(setCompetencies(newCompetence));
  };

  return (
    <div className="filterItem filterItem__salary">
      <div className="filterItem-title">Компетенции</div>
      <div className="competencies-field-wrapper">
        <Select
          closeMenuOnSelect={false}
          // components={animatedComponents}
          // defaultValue={}
          hideSelectedOptions={true}
          isMulti
          options={options}
          placeholder="Выбрать компетенцию"
          onChange={handlerOnChangeValue}
          classNamePrefix="custom-multiselect"
          tabSelectsValue={true}
        />
      </div>
    </div>
  );
}

export default CompetenciesField;