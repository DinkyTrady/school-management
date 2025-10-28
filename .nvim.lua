vim.api.nvim_create_autocmd({'BufEnter', 'BufRead', 'BufNew'}, {
  group = vim.api.nvim_create_augroup('change_filetype', {clear = true}),
  callback = function (args)
    if vim.bo[args.buf].filetype == 'html' then
      vim.bo[args.buf].filetype = 'htmldjango'
    end
  end
})
