<h2>List submission types</h2>

<table>

% if len(c.submissiontype_collection) > 0:
<tr>
<th>Name</th>
</tr>
% #endif

% for st in c.submissiontype_collection:
<tr>
	<td><% h.link_to(st.name, url=h.url(action='view', id=st.id)) %></td>
% 	if c.can_edit:
%		for action in ['edit', 'delete']:
	<td><% h.link_to(action, url=h.url(action=action, id=st.id)) %></td>
%		# endif
%	 #endfor
</tr>
% #endfor
</table>


<%python>
#if c.submissiontype_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.submissiontype_pages.current.previous)) + '  ')
#if c.submissiontype_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.submissiontype_pages.current.next)))

m.write('<br />')
if c.can_edit:
    m.write(h.link_to('New submission type', url=h.url(action='new')))
</%python>
 