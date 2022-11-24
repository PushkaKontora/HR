import {createAsyncThunk} from '@reduxjs/toolkit';
import {Generics} from '../../types/generics';
import {ResumeRoutes} from '../../const/api-routes/api-resume-routes';
import {ResumeUser} from '../../types/resume';

export const createResumeAction = createAsyncThunk<void, {user_id: number, data: FormData}, Generics>(
  'resume/create',
  async (arg, {dispatch, extra: api}) => {
    arg.data.append('user_id', arg.user_id.toString());
    await api.post(ResumeRoutes.resume, arg.data);
  }
);

export const updateResumeAction = createAsyncThunk<void, {resume_id: number, data: FormData}, Generics>(
  'resume/update',
  async (arg, {dispatch, extra: api}) => {
    await api.post(ResumeRoutes.resumeByID(arg.resume_id), arg.data);
  }
);

export const publishResumeAction = createAsyncThunk<string, {resume_id: number}, Generics>(
  'resume/publish',
  async (arg, {dispatch, extra: api}) => {
    const res = await api.patch(ResumeRoutes.publish(arg.resume_id));
    return res.data.published_at;
  }
);

export const unpublishResumeAction = createAsyncThunk<void, {resume_id: number}, Generics>(
  'resume/unpublish',
  async (arg, {dispatch, extra: api}) => {
    await api.patch(ResumeRoutes.unpublish(arg.resume_id));
  }
);