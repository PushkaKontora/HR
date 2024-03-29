import '../modal-edit-vacancy/modal-edit-vacancy.scss';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import React, {ChangeEvent, useCallback, useEffect, useState} from 'react';
import {ExpectedExperience, ExpectedExperienceNameString, expectedExperienceShortVersion, SortingVacancyTypes, TypeRequestVacancyModal} from '../../const';
import {createVacancy, getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';
import {DepartmentsShortVersions, setIsEditorVacancyFlag, setIsOpenCreateVacancyModal, setIsStartRequestChangeVacancy} from '../../features/vacancy/vacancy-slice';
import Select, {SingleValue} from 'react-select';
import Modal from '../../reused-components/modal/modal';
import EmployerCreatingNewVacancy from '../employer-creating-new-vacancy/employer-creating-new-vacancy';
import {GrayButton} from '../styled/buttons/gray-button';
import {BlueButton} from '../styled/buttons/blue-button';
import {CreateVacancyParams} from '../../types/create-vacancy-params';
import ModalBtnStatusVacancy from '../modal-btn-status-vacancy/modal-btn-status-vacancy';
import cl from 'classnames';
import '../../styles/btn-blue-disabled.scss';

function ModalCreateVacancy() {
  const typeRequestModalVacancy = useAppSelector((state) => state.vacancy.typeRequestModalVacancy);
  const isPublishedVacancy = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const isOpenCreateVacancyModalFromRedux = useAppSelector((state) => state.vacancy.isOpenCreateVacancyModal);
  const isEditorVacancyText = useAppSelector((state) => state.vacancy.editorTextVacancy);
  const isEditorVacancyFlag = useAppSelector((state) => state.vacancy.isEditorVacancyFlag);
  const isStartRequestChangeVacancy = useAppSelector((state) => state.vacancy.isStartRequestChangeVacancy);
  const departmentID = useAppSelector((state) => state.general.user?.department.id);
  const [isOpenCreateVacancy, setIsOpenCreateVacancy] = useState(isOpenCreateVacancyModalFromRedux);
  const [isPublishStatus, setIsPublishStatus] = useState(isPublishedVacancy);
  const [nameVacancy, setNameVacancy] = useState('');
  const [experience, setExperience] = useState<ExpectedExperience>(ExpectedExperience.NO_EXPERIENCE);
  const [minSalary, setMinSalary] = useState<number | null>(null);
  const [maxSalary, setMaxSalary] = useState<number | null>(null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isStartRequestChangeVacancy === true
      && departmentID
      && typeRequestModalVacancy === TypeRequestVacancyModal.CREATE) {
      const vacancyBody: CreateVacancyParams = {
        name: nameVacancy,
        description: isEditorVacancyText,
        expected_experience: experience,
        salary_from: minSalary,
        salary_to: maxSalary,
        published: isPublishStatus,
        department_id: departmentID
      };
      dispatch(createVacancy({data: vacancyBody}))
        .then(() => {
          dispatch(getVacanciesForEmployer({isPublished: isPublishedVacancy, idDepartment: departmentID, offset: 0}))
            .then(() => {
              dispatch(setIsEditorVacancyFlag(false));
              setIsOpenCreateVacancy(false);
            });
        });

      dispatch(setIsStartRequestChangeVacancy(false));
    }
  }, [isEditorVacancyText, isEditorVacancyFlag]);


  useEffect(() => {
    setIsOpenCreateVacancy(isOpenCreateVacancyModalFromRedux);
  }, [isOpenCreateVacancyModalFromRedux]);

  useEffect(() => {
    dispatch(setIsOpenCreateVacancyModal(isOpenCreateVacancy));
  }, [isOpenCreateVacancy]);

  const handleChangeNameVacancy = (e: ChangeEvent<HTMLInputElement>) => {
    setNameVacancy(e.target.value);
  };

  const onHandlerChangeExpectedExperience = (e: SingleValue<DepartmentsShortVersions>) => {
    if (e?.label) {
      const valueExp = Object.keys(ExpectedExperienceNameString).find(key => ExpectedExperienceNameString[key] === e.label);
      if (valueExp) {
        setExperience(valueExp as ExpectedExperience);
      }
    }
  };

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    const minValue = e.target.value;
    if (minValue) {
      setMinSalary(Number(minValue));
    } else {
      setMinSalary(null);
    }
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    const maxValue = e.target.value;
    if (maxValue) {
      setMaxSalary(Number(maxValue));
    } else {
      setMaxSalary(null);
    }
  };

  const handlerClickCreateVacancy = () => {
    if (nameVacancy.length > 0 && !(maxSalary !== null && minSalary !== null && maxSalary <= minSalary)) {
      dispatch(setIsEditorVacancyFlag(true));
    }
  };

  const handleUndoAction = (e: any) => {
    e.preventDefault();
    setIsOpenCreateVacancy(false);
  };


  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={1026}
      active={isOpenCreateVacancy}
      setActive={setIsOpenCreateVacancy}
    >
      <div className="edit-modal-item edit-modal-item__header">
        <div className="header header__title">Создание новой вакансии</div>
        <div className="header header__explanation">Заполните обязательные поля для создания вакансии</div>
      </div>
      <div className="edit-modal-item edit-modal-item__content">
        <div className="content-item">
          <div className="name-field">
            Статус вакансии*
          </div>
          <ModalBtnStatusVacancy isPublishStatus={isPublishStatus} setIsPublishStatus={setIsPublishStatus}/>
        </div>
        <div className="content-item">
          <div className="name-field">
            Название вакансии*
          </div>
          <input
            type="text"
            onChange={handleChangeNameVacancy}
            className="input-name-vacancy"
            value={nameVacancy}
            placeholder="Введите название"
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Опыт работы*
          </div>
          <Select
            className="basic-single"
            classNamePrefix="select"
            styles={{
              control: (baseStyles, state) => ({
                ...baseStyles,
                width: '252px'
              }),
            }}
            name=""
            options={expectedExperienceShortVersion}
            onChange={onHandlerChangeExpectedExperience}
            placeholder={ExpectedExperienceNameString[experience as ExpectedExperience]}
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Зарплата
          </div>
          <div className="salaryInput-wrapper">
            <div className="text-field-salary text-field-salary__min">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                onChange={handleChangeMinSalary}
                placeholder="min"
              />
            </div>
            <div className="text-field-salary text-field-salary__max">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                onChange={handleChangeMaxSalary}
                placeholder="max"
              />
            </div>
          </div>
        </div>
        <div className="content-item content-item__description">
          <div className="name-field">
            Описание вакансии*
          </div>
          <EmployerCreatingNewVacancy typeViewToolbar={TypeRequestVacancyModal.CREATE}/>
        </div>
      </div>
      <div className="edit-modal-item edit-modal-item__nav">
        <GrayButton as="button" onClick={handleUndoAction}>Отмена</GrayButton>
        <BlueButton as="button" className={cl({'disabledBlueBtn': nameVacancy.length <= 0 || (maxSalary !== null && minSalary !== null && maxSalary <= minSalary)})} onClick={handlerClickCreateVacancy}>
          Создать вакансию
        </BlueButton>
      </div>
    </Modal>
  );
}

export default ModalCreateVacancy;