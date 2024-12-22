import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';

import TeamMember from '@/app/(customer)/components/teamMember';

describe('TeamMember Component', () => {
  const mockProps = {
    img: { src: '/path/to/image.jpg' },
    bakerName: 'John Doe',
    positionBaker: 'Head Baker',
  };

  it('renders baker name', () => {
    render(<TeamMember {...mockProps} />);
    const bakerName = screen.getByText(/John Doe/i);
    expect(bakerName).toBeInTheDocument();
  });

  it('renders baker position', () => {
    render(<TeamMember {...mockProps} />);
    const position = screen.getByText(/Head Baker/i);
    expect(position).toBeInTheDocument();
  });

});