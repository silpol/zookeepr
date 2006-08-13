import smtplib

from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, c, g, h, render, render_response, request
from zookeepr.lib.validators import BaseSchema, SubmissionTypeValidator
from zookeepr.model import Person, SubmissionType, Submission
    
class RegistrationSchema(Schema):
    email_address = validators.String(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    fullname = validators.String()

class SubmissionSchema(Schema):
    title = validators.String(not_empty=True)
    abstract = validators.String(not_empty=True)
    type = SubmissionTypeValidator()
    experience = validators.String()
    url = validators.String()
    attachment = validators.String()
    assistance = validators.Bool()
    
class NewCFPSchema(BaseSchema):
    registration = RegistrationSchema()
    submission = SubmissionSchema()
    pre_validators = [NestedVariables]

class CfpController(BaseController):
    def index(self):
        return render_response("cfp/list.myt")

    def submit(self):
        c.cfptypes = g.objectstore.query(SubmissionType).select()

        errors = {}
        defaults = dict(request.POST)

        new_reg = Person()
        new_sub = Submission()

        c.registration = new_reg
        c.submission = new_sub
        
        if request.method == 'POST' and defaults:
            result, errors = NewCFPSchema().validate(defaults)

            if not errors:
                # update the objects with the validated form data
                for k in result['submission']:
                    setattr(new_sub, k, result['submission'][k])
                for k in result['registration']:
                    setattr(new_reg, k, result['registration'][k])

                g.objectstore.save(new_reg)
                g.objectstore.save(new_sub)

                new_reg.submissions.append(new_sub)

                g.objectstore.flush()

                s = smtplib.SMTP("localhost")
                # generate the message from a template
                body = render('cfp/submission_response.myt', id=new_reg.url_hash, fragment=True)
                s.sendmail("seven-contact@lca2007.linux.org.au", new_reg.email_address, body)
                s.quit()

                return render_response('cfp/thankyou.myt')

        # unmangle the errors
        good_errors = {}
        for key in errors.keys():
            for subkey in errors[key].keys():
                good_errors[key + "." + subkey] = errors[key][subkey]

        return render_response("cfp/new.myt", defaults=defaults, errors=good_errors)
