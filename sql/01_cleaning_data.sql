with using_cols as (
	select role, purpose, expected_class, challenges, source, expected_model, using_exp_evaluate, looking_evaluate, advantage, disadvantage
	from survey_responses_raw
),
count_null_table as (
	select 
		count(*) filter(where role is null or trim(role) = '') null1,
		count(*) filter(where purpose is null or trim(purpose) = '') null2,
		count(*) filter(where expected_class is null or trim(expected_class) = '') null3,
		count(*) filter(where challenges is null or trim(challenges) = '') null4,
		count(*) filter(where source is null or trim(source) = '') null5,
		count(*) filter(where expected_model is null or trim(expected_model) = '') null6,
		count(*) filter(where using_exp_evaluate is null or trim(using_exp_evaluate::text) = '') null7,
		count(*) filter(where looking_evaluate is null or trim(looking_evaluate::text) = '') null8,
		count(*) filter(where advantage is null or trim(advantage) = '') null9,
		count(*) filter(where disadvantage is null or trim(disadvantage) = '') null10
	from using_cols
),
null_table as (
	select 
		case when role is null or trim(role) = '' then null else role end as role,
		case when purpose is null or trim(purpose) = '' then null else purpose end as purpose,
		case when expected_class is null or trim(expected_class) = '' then null else expected_class end as expected_class,
		case when challenges is null or trim(challenges) = '' then null else challenges end as challenges,
		case when source is null or trim(source) = '' then null else source end as source,
		case when expected_model is null or trim(expected_model) = '' then null else expected_model end as expected_model,
		case when using_exp_evaluate is null or trim(using_exp_evaluate::text) = '' then null else using_exp_evaluate end as using_exp_evaluate,
		case when looking_evaluate is null or trim(looking_evaluate::text) = '' then null else looking_evaluate end as looking_evaluate,
		case when advantage is null or trim(advantage) = '' then null else advantage end as advantage,
		case when disadvantage is null or trim(disadvantage) = '' then null else disadvantage end as disadvantage
	from using_cols
)
select * from null_table
where expected_class is null