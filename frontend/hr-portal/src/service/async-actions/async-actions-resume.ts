import {createAsyncThunk} from '@reduxjs/toolkit';
import {Generics} from '../../types/generics';
import {ResumeRoutes} from '../../const/api-routes/api-resume-routes';
import {ResumeUser} from '../../types/resume';
import {Vacancy} from '../../types/vacancy';

export const ResumeWishListSortBy = {
  published_at_desc: 'published_at_desc',
  published_at_asc: 'published_at_asc',
  added_at_desc: 'added_at_desc'
};

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

export const deleteDocument = createAsyncThunk<void, number, Generics>(
  'resume/deleteDocument',
  async (resume_id, {dispatch, extra: api}) => {
    await api.delete(ResumeRoutes.document(resume_id));
  }
);

export const getResumeWishlist = createAsyncThunk<ResumeUser[], string, Generics>(
  'resume/wishlist',
  async (arg, {dispatch, extra: api}) => {
    const res = await api.get(ResumeRoutes.wishlist(arg));
    return res.data;
  }
);

export const addToResumeWishlist = createAsyncThunk<void, number, Generics>(
  'resume/addToWishlist',
  async (resumeId, {dispatch, extra: api}) => {
    await api.post(ResumeRoutes.modifyWishlist(resumeId));
    await api.get(ResumeRoutes.wishlist(ResumeWishListSortBy.added_at_desc));
  }
);

export const deleteToResumeWishlist = createAsyncThunk<void, number, Generics>(
  'resume/deleteToWishlist',
  async (resumeId, {dispatch, extra: api}) => {
    await api.delete(ResumeRoutes.modifyWishlist(resumeId));
    await api.get(ResumeRoutes.wishlist(ResumeWishListSortBy.added_at_desc));
  }
);
