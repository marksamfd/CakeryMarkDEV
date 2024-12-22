import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import AdminHeader from '@/app/(customer)/components/adminHeader';

describe('AdminHeader Component', () => {
  it('renders "Manage Products" dropdown', () => {
    render(<AdminHeader pos="Admin" />);
    
    const dropdown = screen.getByText(/Manage Products/i);
    expect(dropdown).toBeInTheDocument();
  });


  it('renders "Manage Vouchers" dropdown', () => {
    render(<AdminHeader pos="Admin" />);
    
    const dropdown = screen.getByText(/Manage Vouchers/i);
    expect(dropdown).toBeInTheDocument();
  });


});

